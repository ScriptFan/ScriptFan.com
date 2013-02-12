#-*-coding:utf-8-*-
from datetime import datetime
from flask import Blueprint, session, request, url_for, redirect, abort
from flask import render_template, flash
from flask import current_app as app
from flask.ext import login
from flask.ext.login import current_user
from flask.ext.openid import COMMON_PROVIDERS
from scriptfan.extensions import db, oid, login_manager
from scriptfan.models import User, UserOpenID
from scriptfan.forms.user import SignupForm, SigninForm, EditProfileForm, EditPasswordForm, EditSlugForm, ManageOpenIDForm

userapp = Blueprint("user", __name__)

class Anonymous(login.AnonymousUser):
    user = User(nickname=u'游客', email='')

class LoginUser(login.UserMixin):
    """Wraps User object for Flask-Login"""

    def __init__(self, user):
        self.id = user.id
        self.user = user

login_manager.anonymous_user = Anonymous
login_manager.login_view = 'user.signin'
login_manager.login_message = u'需要登陆后才能访问本页'

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user and LoginUser(user) or None

def login_user(user, remember=False):
    """ 登陆用户并更新最近登陆时间 """
    login.login_user(LoginUser(user), remember=remember)
    user.login_time = datetime.now()
    app.logger.info('* Updated current user: %s, %s', user.id, user.email)

# 开发资料修改页面中的OpenID绑定功能
# FIXME: 第一次接触OpenID，实现得有点绕，是否还有漏洞没考虑到？一起讨论吧
@userapp.route('/openid/manage', methods=['GET', 'POST'])
@login.login_required
def openid_manage():
    form = ManageOpenIDForm(csrf_enabled=False)
    if form.validate_on_submit():
        method = form.method.data
        provider = form.provider.data
        if method == 'add':
            return redirect(url_for('user.openid_add', provider=provider))
        elif method == 'delete':
            return _delete_openid(provider)
    registed_providers = [openid.provider 
            for openid in current_user.user.openids]
    providers = [(provider, provider in registed_providers)
            for provider in COMMON_PROVIDERS]
    return render_template('user/openid.html', providers = providers, form=form)

# 解除绑定的实现
def _delete_openid(provider):
    user = current_user.user
    openid = UserOpenID.query.filter_by(provider=provider, user=user).first()
    if openid:
        if len(user.openids) < 2 and not user.password:
            flash(u'你只绑定了唯一一个OpenID，并且还没有设置密码, 不可以解除绑定哦！',
                    'warning')
        else:
            db.session.delete(openid)
            flash(u'成功解除与 <strong>%s</strong> 的绑定!' % openid.provider, 
                    'success')
    else:
        flash(u'解除OpenID绑定时发生了错误!', 'error')
    return redirect(url_for('user.openid_manage'))

# 添加绑定的实现
@userapp.route('/openid/add/<provider>/', methods=['GET'])
@login.login_required
@oid.loginhandler
def openid_add(provider):
    next_url = url_for('user.openid_manage')
    if provider not in COMMON_PROVIDERS:
        app.logger.warning('Invalid openid provider: %s' % provider)
        flash(u'暂不支持绑定到 <strong>%s</strong> ' % provider, 'warning')
        return redirect(next_url)
    # 这里默认一个provider只能绑定一次
    openid = UserOpenID.query.filter_by(provider=provider, user=current_user.user).first()
    if openid:
        app.logger.warning('provider: %s has already bind to this acccount' % provider)
        flash(u'你已经绑定到 <strong>%s</stong> 了' % provider, 'warning')
        return redirect(next_url)
    session['openid_provider'] = provider
    # 用于openid回调函数create_or_login判断是登陆还是绑定
    session['openid_user_id'] = current_user.user.id
    app.logger.info('Regist openid: %s, callback: %s', provider, next_url)
    openid_error = oid.fetch_error()
    if openid_error:
        app.logger.error(openid_error)
        flash(u'绑定OpenID失败: ' + openid_error)
        return redirect(next_url)
    app.logger.info(COMMON_PROVIDERS.get(provider))
    return oid.try_login(COMMON_PROVIDERS.get(provider), \
                         ask_for=['email', 'fullname', 'nickname'])

@userapp.route('/openid/<provider>/', methods=['GET'])
@oid.loginhandler
def openid(provider, next=None):
    if current_user.is_authenticated():
        app.logger.info('User authenticated, redirecting to profile page')
        return redirect(url_for('user.profile'))
    
    next_url = oid.get_next_url()
    if provider not in COMMON_PROVIDERS:
        app.logger.warning('Invalid openid provider: %s' % provider)
        flash(u'暂不支持 <strong>%s</strong> 登陆' % provider, 'warning')
        return redirect(next_url)

    session['openid_provider'] = provider
    app.logger.info('Signin with openid: %s, callback: %s', provider, next_url)

    openid_error = oid.fetch_error()
    if openid_error:
        app.logger.error(openid_error)
        flash(u'登陆失败: ' + openid_error)
        return redirect(oid.get_next_url())

    app.logger.info(COMMON_PROVIDERS.get(provider))
    return oid.try_login(COMMON_PROVIDERS.get(provider), \
                         ask_for=['email', 'fullname', 'nickname'])


@userapp.route('/signin/', methods=['GET', 'POST'])
def signin():
    # 如果用户已经登陆，跳转到用户资料页面
    if current_user.is_authenticated():
        return redirect(url_for('user.profile'))
   
    form = SigninForm(csrf_enabled=False)
    
    if form.validate_on_submit():
        app.logger.info('Signin user: %s', form.email.data)
        login_user(form.user, remember=form.remember)
        flash(u'登陆成功', 'success')
        return form.redirect('user.profile')
   
    return render_template('user/signin.html', form=form)


@oid.after_login
def create_or_login(resp):
    app.logger.info('OpenID Response: %s, %s, %s',
            resp.email, resp.fullname, resp.nickname)
    user_id = session.get('openid_user_id', None)
    session.pop('openid_user_id', None)
    # 这里分为两种情况
    if user_id:
        # 绑定到已有帐号
        return _regist_openid(user_id, resp)
    else:
        # 用该OpenID登陆
        return _create_or_login(resp)

# 这个方法用于绑定OpenID到已有帐号
def _regist_openid(user_id, resp):
    redirect_url = url_for('user.openid_manage')
    # 清理Session里的键，这样不影响以后的登陆
    provider = session.get('openid_provider', None)
    session.pop('openid_provider', None)
    if provider and current_user.is_authenticated() \
            and user_id == current_user.user.id:
        # 检查该openid是否已经存在
        openid = UserOpenID.query.filter_by(openid=resp.identity_url).first()
        if openid:
            flash(u'这个OpenID已经被绑定了', 'warning')
            return redirect(redirect_url)
        # 检查openid中注册的邮箱是否被其它用户占用
        user = User.query.filter_by(email=resp.email).first()
        if user and user.id != user_id:
            flash(u'邮箱 <strong>%s</strong> 已经被注册，如果你是该帐户的拥有者，请用该邮箱登陆后再绑定OpenID' % resp.email, 'warning')
            return redirect(redirect_url)
        # 绑定这个OpenID
        openid = UserOpenID(openid=resp.identity_url, provider=provider)
        current_user.user.openids.append(openid)
        app.logger.info('bind openid: %s to user: %s', resp.identity_url, current_user.user)
        flash(u'成功绑定到 <strong>%s</strong> 帐户，你可以用该帐户直接登陆了！' % provider, 'success')
        return redirect(redirect_url)
    else:
        # 其它情况下不给用户具体信息
        flash(u'绑定OpenID失败!', 'error')
        return redirect(redirect_url)

# 这个方法用OpenID登陆
def _create_or_login(resp):
    # 如果openid未注册，先自动注册用户，并绑定openid
    user = User.query.join(User.openids) \
                     .filter(UserOpenID.openid==resp.identity_url).first()

    # 如果OpenID尚未绑定用户，直接创建用户并绑定OpenID
    if not user:
        # 如果邮箱已经被注册，提示手工绑定
        if User.query.filter_by(email=resp.email).first():
            flash(u'邮箱 <strong>%s</strong> 已经被注册，如果你是该帐户的拥有者，请登陆后再绑定OpenID' % resp.email, 'warning')
            return redirect(url_for('user.signin'))
        
        # 邮箱没有注册，自动创建帐户并登陆
        app.logger.info('Creating user with openid: %s', resp.identity_url)
        user = User(email=resp.email, nickname=resp.nickname or resp.fullname)
        openid = UserOpenID(openid=resp.identity_url, provider=session['openid_provider'])
        user.openids.append(openid)
        db.session.add(user)
        db.session.commit()

        flash(u'帐号已经创建, 可以在资料<a href="%s">修改页面</a>补充密码等信息'% url_for('user.general'), 'success')

    app.logger.info('Signin user: %s', user.email)
    login_user(user, remember=True)
    flash(u'登陆成功')

    return redirect(oid.get_next_url())

@userapp.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated():
        return redirect(url_for('user.profile'))
    
    form = SignupForm(csrf_enabled=False)
    app.logger.info('Signup with email: %(email)s, nickname: %(nickname)s', form.data)
    
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.set_password(form.password1.data)
        db.session.add(user)
        app.logger.info(u'New user added: %s', user)
        flash(u'注册成功', 'success')
        return redirect(url_for('user.signin'))
    
    return render_template('user/signup.html', form=form)

@userapp.route('/profile/')
@userapp.route('/profile/<slug_or_id>')
@login.login_required
def profile(slug_or_id=None):
    if slug_or_id:
        if slug_or_id.isdigit():
            user = User.query.get(int(slug_or_id)).first()
        else:
            user = User.query.filter_by(slug=slug_or_id).first()
        return user and render_template('user/profile.html', user=user) or abort(404)
    else:
        return render_template('user/profile.html', user=current_user.user)

@userapp.route('/general', methods=['GET', 'POST'])
@login.login_required
def general():
    form = EditProfileForm(csrf_enabled=False)
    if form.validate_on_submit():
        app.logger.info(u'* Updating user information...')
        app.logger.info(u'Form data: %s', repr(form.data))
        form.populate_obj(current_user.user)
        flash(u'用户资料已经更新', 'success')
        return form.redirect('user.general')
    
    # 如果是编辑用户信息，则使用用户当前信息填充表单
    form.process(obj=current_user.user)
    return render_template('user/general.html', form=form)

    # TODO 处理更新用户资料的请求
    # TODO 用户照片上传

# TODO: 用户找回密码功能

# 更新用户slug功能
@userapp.route('/slug', methods=['GET', 'POST'])
@login.login_required
def slug():
    form = EditSlugForm()
    if form.validate_on_submit():
        form.populate_obj(current_user.user)
        flash(u'修改域名已经设置', 'success')
        return redirect(url_for('user.profile', slug=current_user.user.slug))

    form.process(obj=current_user.user)
    return render_template('user/slug.html', form=form, skip_slug_info=True)


@userapp.route('/password', methods=['GET', 'POST'])
@login.login_required
def password():
    form = EditPasswordForm(csrf_enabled=False)
    if form.validate_on_submit():
        current_user.user.set_password(form.password.data)
        flash(u'用户密码已经更新', 'success')
        return form.redirect('user.general')

    form.errors and flash(u'用户密码未能更新', 'error')
    return render_template('user/password.html', form=form, skip_password_info=True)

@userapp.route('/email')
@login.login_required
def editemail():
    return 'email'

@userapp.route('/signout/', methods=['GET'])
@login.login_required
def signout():
    login.logout_user()
    if 'openid_provider' in session:
        del session['openid_provider']
    return redirect(url_for('site.index'))

