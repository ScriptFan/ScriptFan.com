# -*- coding: utf-8 -*-
from datetime import datetime
import uuid
from flask import Blueprint, session, request, url_for, redirect, abort, g, jsonify
from flask import render_template, flash
from flask import current_app as app
from flask.ext import login
from flask.ext.login import current_user
from flask.ext.openid import COMMON_PROVIDERS
from flask.ext.babel import gettext as _
from flask.ext.principal import Identity, AnonymousIdentity, identity_changed, identity_loaded
from flask_mail import Message

from scriptfan import db, oid, mail, login_manager
from scriptfan.models import User, UserOpenID
from scriptfan.functions import roles_required
from scriptfan.forms.user import SignupForm, SigninForm, EditProfileForm, \
                                 EditPasswordForm, EditSlugForm, \
                                 ManageOpenIDForm, ResetStep1Form, ResetStep2Form

blueprint = Blueprint('users', __name__)

class Anonymous(login.AnonymousUser):
    user = User(nickname=u'游客', email='')

class LoginUser(login.UserMixin):
    """Wraps User object for Flask-Login"""

    def __init__(self, user):
        self.id = user.id
        self.user = user

login_manager.anonymous_user = Anonymous
login_manager.login_view = 'users.signin'
login_manager.login_message = u'需要登陆后才能访问本页'

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user and LoginUser(user) or None

def login_user(user, remember=False):
    """ 登陆用户并更新最近登陆时间 """
    login.login_user(LoginUser(user), remember=remember)
    user.login_time = datetime.now()

# 开发资料修改页面中的OpenID绑定功能
# FIXME: 第一次接触OpenID，实现得有点绕，是否还有漏洞没考虑到？一起讨论吧
@blueprint.route('/openid/manage', methods=['GET', 'POST'])
@login.login_required
def openid_manage():
    g.actived_navitem = 'openids'

    form = ManageOpenIDForm(csrf_enabled=False)
    if form.validate_on_submit():
        method = form.method.data
        provider = form.provider.data
        if method == 'add':
            return redirect(url_for('users.openid_add', provider=provider))
        elif method == 'delete':
            return _delete_openid(provider)
    registed_providers = [openid.provider 
            for openid in current_user.user.openids]
    providers = [(provider, provider in registed_providers)
            for provider in COMMON_PROVIDERS]
    return render_template('users/openid.html', providers = providers, form=form)

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
    return redirect(url_for('users.openid_manage'))

# 添加绑定的实现
@blueprint.route('/openid/add/<provider>/', methods=['GET'])
@login.login_required
@oid.loginhandler
def openid_add(provider):
    next_url = url_for('users.openid_manage')
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

@blueprint.route('/openid/<provider>/', methods=['GET'])
@oid.loginhandler
def openid(provider, next=None):
    if current_user.is_authenticated():
        app.logger.info('User authenticated, redirecting to profile page')
        return redirect(url_for('users.profile'))
    
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


@blueprint.route('/signin/', methods=['GET', 'POST'])
def signin():
    # 如果用户已经登陆，跳转到用户资料页面
    if current_user.is_authenticated():
        return redirect(url_for('users.profile'))
   
    form = SigninForm(csrf_enabled=False)
    
    if form.validate_on_submit():
        app.logger.info('Signin users: %s', form.email.data)
        login_user(form.user, remember=form.remember)
        identity_changed.send(app._get_current_object(), identity=Identity(current_user.user.id))
        flash(_('views.users.signin.signin_success'), 'success')
        return form.redirect('users.profile')
   
    return render_template('users/signin.html', form=form)


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
    redirect_url = url_for('users.openid_manage')
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
        app.logger.info('bind openid: %s to users: %s', resp.identity_url, current_user.user)
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
            return redirect(url_for('users.signin'))
        
        # 邮箱没有注册，自动创建帐户并登陆
        app.logger.info('Creating users with openid: %s', resp.identity_url)
        user = User(email=resp.email, nickname=resp.nickname or resp.fullname)
        openid = UserOpenID(openid=resp.identity_url, provider=session['openid_provider'])
        user.openids.append(openid)
        db.session.add(user)
        db.session.commit()

        _send_welcome_email(user)

        flash(u'帐号已经创建, 可以在资料<a href="%s">修改页面</a>补充密码等信息'% url_for('users.general'), 'success')

    app.logger.info('Signin users: %s', user.email)
    login_user(user, remember=True)
    flash(u'登陆成功')

    return redirect(oid.get_next_url())

@blueprint.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated():
        return redirect(url_for('users.profile'))
    
    form = SignupForm(csrf_enabled=False)
    app.logger.info('Signup with email: %(email)s, nickname: %(nickname)s', form.data)
    
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.set_password(form.password1.data)
        db.session.add(user)
        app.logger.info(u'New users added: %s', user)
        _send_welcome_email(user)
        flash(u'注册成功', 'success')
        return redirect(url_for('users.signin'))
    
    return render_template('users/signup.html', form=form)

# FIXME: Slug should not be same as an exists user_id
@blueprint.route('/profile/', methods=['GET'])
@blueprint.route('/profile/<slug_or_id>', methods=['GET'])
@login.login_required
def profile(slug_or_id=None):
    if slug_or_id:
        user = User.get_by_slug_or_id(slug_or_id)
        return user and render_template('users/profile.html', user=user) or abort(404)
    else:
        return render_template('users/profile.html', user=current_user.user)

@blueprint.route('/profile/<slug_or_id>', methods=['POST'])
@roles_required('admin', 'root')
def update_role(slug_or_id=None):
    """ 更改用户级别 """

    privilege = request.form.get('privilege', '')
    if slug_or_id and privilege.isdigit():
        privilege = int(privilege)

        user = User.get_by_slug_or_id(slug_or_id)
        if user and current_user.user.privilege > user.privilege and current_user.user.privilege > privilege:
            user.privilege = privilege
            msg = u'<strong>%s</strong> 已经被设置为 <strong>%s</strong>' % (user.nickname, user.privilege_name)
            flash(msg, 'success')
            return msg

    flash(u'更新用户出错，请重试！', 'error')
    return abort(404)


@blueprint.route('/general', methods=['GET', 'POST'])
@login.login_required
def general():
    g.actived_navitem = 'general'

    form = EditProfileForm(csrf_enabled=False)
    if form.validate_on_submit():
        app.logger.info(u'* Updating users information...')
        app.logger.info(u'Form data: %s', repr(form.data))
        form.populate_obj(current_user.user)
        flash(u'用户资料已经更新', 'success')
        return form.redirect('users.general')
    
    # 如果是编辑用户信息，则使用用户当前信息填充表单
    form.process(obj=current_user.user)
    return render_template('users/general.html', form=form)

    # TODO 处理更新用户资料的请求
    # TODO 用户照片上传

# 更新用户slug功能
@blueprint.route('/slug', methods=['GET', 'POST'])
@login.login_required
def slug():
    g.actived_navitem = 'slug'

    form = EditSlugForm()
    if form.validate_on_submit():
        form.populate_obj(current_user.user)
        flash(u'修改域名已经设置', 'success')
        return redirect(url_for('users.profile', slug_or_id=current_user.user.slug))

    form.process(obj=current_user.user)
    return render_template('users/slug.html', form=form, skip_slug_info=True)

def _send_welcome_email(user):
    """ 发送欢迎邮件 """

    try:
        app.logger.info('Sending welcome email to %s', user.email)
        msg = Message(u'欢迎来到ScriptFan', recipients=[user.email])
        msg.html = render_template('users/email/welcome.html', user=user)
        # FIXME: 邮件发送使用异步方式，避免用户等待太长时间
        mail.send(msg)
        app.logger.info('Mail sent successfully.')
    except Exception, e:
        app.logger.info(e.message)
        app.logger.error('Failed to send welcome reset mail, because: %s', e)

def _send_reset_email(user, token):
    """ 发送密码重置邮件 """

    try:
        app.logger.info('Sending reset email to %s with token %s', user.email, token)
        msg = Message(u'ScriptFan密码重置', recipients=[user.email])
        msg.html = render_template('users/email/reset.html', user=user, token=token)
        # FIXME: 邮件发送使用异步方式，避免用户等待太长时间
        mail.send(msg)
        app.logger.info('Mail sent successfully.')
        return True
    except Exception, e:
        app.logger.info(e.message)
        app.logger.error('Failed to send password reset mail, because: %s', e)
        return False

def _send_reset_success_email(user):
    """ 发送重置通知邮件 """

    try:
        app.logger.info('Sending email confirm notification to %s', user.email)
        msg = Message(u'你在 ScriptFan 的密码已经重置！', recipients=[user.email])
        msg.html = render_template('users/email/reset_success.html', user=user)
        # FIXME: 邮件发送使用异步方式，避免用户等待太长时间
        mail.send(msg)
        app.logger.info('Mail sent successfully.')
    except Exception, e:
        app.logger.info(e.message)
        app.logger.error('Failed to send email reset notification mail, because: %s', e)


@blueprint.route('/reset/step1', methods=['GET', 'POST'])
def reset_step1():
    """ 重置密码第一步，发送重置链接邮件 """

    # TODO: 相关文字的国际化处理
    form = ResetStep1Form()
    if form.validate_on_submit():
        app.logger.info('User %s request to reset password.', form.user.nickname)
        token = uuid.uuid4().hex

        if _send_reset_email(form.user, token):
            session['reset_email'] = form.user.email
            session['reset_token'] = token
            flash(u'密码重置邮件已经发送至 <strong>%s</strong> 请前往收件箱查收。' % form.user.email, 'success')
            return form.redirect('home.index')

        flash(u'邮件发送失败，请稍候再试', 'error')

    return render_template('users/reset_step1.html', form=form)

def _valid_reset_token():
    """ 验证重置口令及邮件地址是否匹配 """
    email, token = request.args.get('email'), request.args.get('token')
    app.logger.info('Validating email reset with email: %s and token: %s', email, token)
    return session.get('reset_email') and \
           session.get('reset_token') and \
           session['reset_email'] == email and \
           session['reset_token'] == token 

@blueprint.route('/reset/step2', methods=['GET', 'POST'])
def reset_step2():
    form = ResetStep2Form()
    if form.validate_on_submit():
        app.logger.info("Updating to new password")

        # FIXME: 密码重置 - 验证用户不存在的情况是否有必要？
        user = User.get_by_email(session['reset_email'])
        user.set_password(form.password.data)
        flash(u'用户密码已经更新', 'success')

        # 清除验证用的 Token
        del session['reset_email']
        del session['reset_token']

        _send_reset_success_email(user)

        return redirect(url_for('users.signin'))

    # 如果邮件及当前token均匹配，则显示重置密码的表单
    if _valid_reset_token(): 
        return render_template('users/reset_step2.html', form=form)
    else:
        flash(u'重置密码链接无效或者已经过期，请重新发送重置密码邮件', 'warning')
        return redirect(url_for('users.reset_step1'))


@blueprint.route('/password', methods=['GET', 'POST'])
@login.login_required
def password():
    g.actived_navitem = 'password'

    form = EditPasswordForm(csrf_enabled=False)
    if form.validate_on_submit():
        current_user.user.set_password(form.password.data)
        flash(u'用户密码已经更新', 'success')
        return form.redirect('users.general')

    form.errors and flash(u'用户密码未能更新', 'error')
    return render_template('users/password.html', form=form, skip_password_info=True)

@blueprint.route('/email')
@login.login_required
def editemail():
    return 'email'

@blueprint.route('/signout/', methods=['GET'])
@login.login_required
def signout():
    login.logout_user()

    for key in ('openid_provider', 'identity.name', 'identity.auth_type', 'identity'):
        session.pop(key, None)

    identity_changed.send(app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('home.index'))


