#!/usr/bin/env python
#-*-coding:utf-8-*-
from datetime import datetime
from flask import Blueprint, session, url_for, redirect, abort
from flask import render_template, flash
from flask import current_app as app
from flask.ext import login
from flask.ext.login import current_user
from flask.ext.openid import COMMON_PROVIDERS
from scriptfan.extensions import db, oid, login_manager
from scriptfan.models import User, UserOpenID
from scriptfan.forms.user import SignupForm, SigninForm, EditProfileForm, EditPasswordForm

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

# TODO: 开发资料修改页面中的OpenID绑定功能

@userapp.route('/openid/<provider>/', methods=['GET'])
@oid.loginhandler
def openid(provider):
    # 如果用户已经登陆，跳转到用户资料页面
    if current_user.is_authenticated():
        return redirect(url_for('user.profile'))

    if provider not in COMMON_PROVIDERS:
        flash(u'暂不支持使用 <strong>%s</strong> 登陆，请联系管理员' % provider, 'warning')
        return redirect(oid.get_next_url()) 

    session['openid_provider'] = provider 
    app.logger.info('* Signin with openid: %s', provider)
    return oid.try_login(COMMON_PROVIDERS.get(provider), \
                         ask_for=['email', 'fullname', 'nickname'])

@userapp.route('/signin/', methods=['GET', 'POST'])
def signin():
    # 如果用户已经登陆，跳转到用户资料页面
    if current_user.is_authenticated():
        return redirect(url_for('user.profile'))
   
    form = SigninForm(csrf_enabled=False)
    
    if form.validate_on_submit():
        app.logger.info('* Signin user: %s', form.email.data)
        login_user(form.user, remember=form.remember)
        flash(u'登陆成功', 'success')
        return form.redirect('user.profile')
    
    if oid.fetch_error():
        flash(oid.fetch_error(), 'error')

    return render_template('user/signin.html', form=form)


@oid.after_login
def create_or_login(resp):
    app.logger.info('* OpenID Response: %s, %s, %s', resp.email, resp.fullname, resp.nickname)
     
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
    app.logger.info(u' * Signup with email: %(email)s, nickname: %(nickname)s', form.data)
    
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.set_password(form.password1.data)
        db.session.add(user)
        app.logger.info(u'New user added: %s', user)
        flash(u'注册成功', 'success')
        return redirect(url_for('user.signin'))
    
    if oid.fetch_error():
        flash(oid.fetch_error(), 'error')
    
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
        if not form.data['slug']:
            form.slug.data = current_user.user.slug
        form.populate_obj(current_user.user)
        flash(u'用户资料已经更新', 'success')
        return form.redirect('user.general')
    
    # 如果是编辑用户信息，则使用用户当前信息填充表单
    form.process(obj=current_user.user)
    return render_template('user/general.html', form=form)

    # TODO 处理更新用户资料的请求
    # TODO 用户照片上传

# TODO: 用户找回密码功能

@userapp.route('/password', methods=['GET', 'POST'])
@login.login_required
def password():
    form = EditPasswordForm(csrf_enabled=False)
    if form.validate_on_submit():
        current_user.user.set_password(form.password.data)
        flash(u'用户密码已经更新', 'success')
        return form.redirect('user.general')
    form.errors and flash(u'用户密码未能更新', 'error')
    return render_template('user/password.html', form=form)

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

