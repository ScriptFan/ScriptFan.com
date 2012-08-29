#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Blueprint, request, session, url_for, redirect, render_template, flash, current_app as app
from flask.ext import wtf, login
from flask.ext.login import current_user
from scriptfan.extensions import db, oid, login_manager
from scriptfan.models import get_user, User, UserOpenID
from scriptfan.forms import *

# import re

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
@oid.loginhandler
def signin():
    if current_user.is_authenticated():
        return redirect(url_for('user.profile'))

    form = SigninForm(csrf_enabled=False, next=oid.get_next_url())
    app.logger.info('>>> Signin user: ' + repr(dict(form.data, password='<MASK>')))
    
    if form.is_submitted() and form.openid_identifier.data:
        session['openid_provider'] = form.openid_provider.data
        session['openid_identifier'] = form.openid_identifier.data
        return oid.try_login(form.openid_identifier.data, ask_for=['email', 'nickname', 'fullname'])

    if form.validate_on_submit():
        login.login_user(LoginUser(form.user), remember=form.remember)
        flash(u'登陆成功')
        # 如果指定了 next ，跳转到 next 页面
        # 如果用户注册了 slug ，则跳转到 slug  的profile 页面，否则跳转到 userid 的 profile 页面
        return redirect(form.next.data or url_for('user.profile'))
    else:
        return render_template('user/signin.html', form=form, openid_error=oid.fetch_error())

@oid.after_login
def create_or_login(resp):
    app.logger.info('>>> OpenID Response: openid=%s, provider=%s', resp.identity_url, session['openid_provider'])
    session['current_openid'] = resp.identity_url
    # TODO: 当使用新的OPENID登陆时，通过邮箱判定该用户以前是否注册过，邮箱未注册时，允许用户自己登陆以绑定帐号
    user_openid = UserOpenID.query.filter_by(openid=resp.identity_url).first()
    if user_openid:
        flash(u'登陆成功')
        app.logger.info(u'Logging with user: ' + user_openid.user.email)
        login.login_user(LoginUser(user_openid.user), remember=True)
        return redirect(oid.get_next_url())
    return redirect(url_for('user.signup', next=oid.get_next_url(), 
        email=resp.email, nickname=resp.nickname or resp.fullname))

@userapp.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated():
        return redirect(url_for('user.profile'))
    
    app.logger.info('request.form: ' + repr(request.values))
    form = SignupForm(request.values, csrf_enabled=False)
    app.logger.info('>>> Signup user: ' + repr(dict(form.data, password='<MASK>')))

    if form.validate_on_submit():
        db.session.add(form.user)
        db.session.commit()
        return redirect(url_for('user.signin'))
    else:
        return render_template('user/signup.html', form=form)

@userapp.route('/profile/')
@userapp.route('/profile/<slug>')
@userapp.route('/profile/<int:user_id>')
@login.login_required
def profile(slug=None, user_id=None):
    # TODO: 用户资料修改及密码修改
    return render_template('user/profile.html')

@userapp.route('/edit')
@login.login_required
def edit():
    form = UserInfoForm(csrf_enabled=False)
    # TODO 处理更新用户资料的请求
    # TODO 用户照片上传
    return render_template('user/edit.html', form=form)

# TODO: 用户找回密码功能

@userapp.route('/password')
@login.login_required
def password():
    return 'password'

@userapp.route('/email')
@login.login_required
def email():
    return 'email'

@userapp.route('/signou/', methods=['GET'])
@login.login_required
def signout():
    login.logout_user()
    del session['current_openid']
    return redirect(url_for('site.index'))
