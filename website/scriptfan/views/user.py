#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Blueprint, session, url_for, redirect, abort
from flask import render_template, flash
from flask import current_app as app
from flask.ext import login
from flask.ext.login import current_user
from scriptfan.extensions import db, oid, login_manager
from scriptfan.models import User, UserOpenID
from scriptfan.forms.user import SignupForm, SigninForm, ProfileForm, EditPassForm

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

@userapp.route('/signin/', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated():
        return redirect(url_for('user.profile'))

    form = SigninForm(csrf_enabled=False)
    app.logger.info('* Signin user: %s', form.email.data)
    
    if form.validate_on_submit():
        login.login_user(LoginUser(form.user), remember=form.remember)
        flash(u'登陆成功', 'success')
        return form.redirect('user.profile')
    return render_template('user/signin.html', form=form)


@oid.after_login
def create_or_login(resp):
    app.logger.info('>>> OpenID Response: openid=%s, provider=%s',
                    resp.identity_url, session['openid_provider'])
    session['current_openid'] = resp.identity_url
    # TODO: 当使用新的OPENID登陆时，通过邮箱判定该用户以前是否注册过，邮箱未注册时，允许用户自己登陆以绑定帐号
    user_openid = UserOpenID.query.filter_by(openid=resp.identity_url).first()
    if user_openid:
        flash(u'登陆成功')
        app.logger.info(u'Logging with user: ' + user_openid.user.email)
        login.login_user(LoginUser(user_openid.user), remember=True)
        return redirect(oid.get_next_url())
    return redirect(url_for('user.signup', next=oid.get_next_url(),
                                           email=resp.email,
                                           nickname=resp.nickname or resp.fullname))

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
    else:
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

@userapp.route('/userinfo/', methods=['GET', 'POST'])
@login.login_required
def edit():
    form = ProfileForm(csrf_enabled=False)
    if form.validate_on_submit():
        app.logger.info(u'* Updating user information...')
        app.logger.info(u'Form data: %s', repr(form.data))
        if not form.data['slug']:
            form.slug.data = current_user.user.slug
        form.populate_obj(current_user.user)
        flash(u'用户资料已经更新', 'success')
        return form.redirect('user.edit')
    
    # 如果是编辑用户信息，则使用用户当前信息填充表单
    form.process(obj=current_user.user)
    return render_template('user/edit.html', form=form)

    # TODO 处理更新用户资料的请求
    # TODO 用户照片上传

# TODO: 用户找回密码功能

@userapp.route('/edit-pass', methods=['GET', 'POST'])
@login.login_required
def edit_pass():
    form = EditPassForm(csrf_enabled=False)
    if form.validate_on_submit():
        current_user.user.set_password(form.password.data)
        flash(u'用户密码已经更新', 'success')
        return form.redirect('user.profile')
    else:
        form.errors and flash(u'用户密码未能更新', 'error')
        return render_template('user/edit_pass.html', form=form)

@userapp.route('/email')
@login.login_required
def editemail():
    return 'email'

@userapp.route('/signout/', methods=['GET'])
@login.login_required
def signout():
    login.logout_user()
    if 'current_openid' in session:
        del session['current_openid']
    return redirect(url_for('site.index'))

