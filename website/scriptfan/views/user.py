#!/usr/bin/env python
#-*-coding:utf-8-*-
import logging
from pprint import pformat
from flask import Blueprint, request, url_for, redirect, render_template, abort, flash, g
from flask.ext import wtf, login
from scriptfan.extensions import *
from scriptfan.models import User, UserInfo
userapp = Blueprint("user", __name__)

class SigninForm(wtf.Form):
    email = wtf.TextField('email', validators=[
        wtf.Required(message=u'请填写电子邮件'), 
        wtf.Email(message=u'无效的电子邮件')])
    password = wtf.PasswordField('password', validators=[
        wtf.Required(message=u'请填写密码'),
        wtf.Length(min=5, max=20, message=u'密应应为5到20位字符')])

    def __init__(self, *args, **kargs):
        wtf.Form.__init__(self, *args, **kargs)
        self.user = None

    def validate(self):
        # 验证邮箱是否注册
        if wtf.Form.validate(self):
            user = User.query.filter_by(email=self.email.data).first()
            if not user:
                self.email.errors.append(u'该邮箱尚未在本站注册')
            else if not user.check_password(self.password.data):
                self.password.errors.append(u'密码错误')
            else:
                self.user = user

        return len(self.errors) == 0

@userapp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignupForm(csrf_enabled=False)
    logging.info('>>> Signup user: ' + repr(dict(form.data, password='<MASK>')))
    if form.validate_on_submit():
        return redirect(url_for('userapp.profile', user_id=form.user.id))
    else:
        return render_template('user/signin.html', form=form)

@oid.after_login
def create_or_login(resp):
    session['openid'] = resp.identity_url
    user = User.query.filter_by(openid=resp.identity_url).first()
    if user is not None:
        flash(u'成功登入')
        session['user'] = str(user.id)
        session.pop('openid')
        g.user = getUserObject(user_id=session['user'])
        return redirect(oid.get_next_url())
    return redirect(url_for('user.signup',
                            next=oid.get_next_url(),
                            nickname=resp.nickname,
                            email=resp.email))

class SignupForm(wtf.Form):
    email = wtf.TextField('email', validators=[
        wtf.Required(message=u'请填写电子邮件'), 
        wtf.Email(message=u'无效的电子邮件')])
    nickname = wtf.TextField('nickname', validators=[
        wtf.Required(message=u'请填写昵称'),
        wtf.Length(min=5, max=20, message=u'昵称应为5到20字符')])
    password = wtf.PasswordField('password', validators=[
        wtf.Required(message=u'请填写密码'),
        wtf.Length(min=5, max=20, message=u'密码应为5到20位字符')])
    repassword = wtf.PasswordField('repassword', validators=[
        wtf.Required(message=u'请填写确认密码'),
        wtf.EqualTo('password', message=u'两次输入的密码不一致')])

    def __init__(self, *args, **kargs):
        wtf.Form.__init__(self, *args, **kargs)
        self.user = None

    def validate(self):
        wtf.Form.validate(self)

        # 验证邮箱是否注册
        if not self.email.errors:
            user = User.query.filter_by(email=self.email.data).first()
            user and self.email.errors.append(u'该邮箱已被注册')
        
        self.user = User(self.nickname.data, self.email.data)
        self.user.set_password(self.password.data)
        return len(self.errors) == 0

@userapp.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegisterForm(csrf_enabled=False)
    logging.info('>>> Signup user: ' + repr(dict(form.data, password='<MASK>')))
    if form.validate_on_submit():
        db.session.add(form.user)
        db.session.commit()
        return redirect(url_for('userapp.signin'))
    else:
        return render_template('user/signup.html', form=form)

@userapp.route('/user/<slug>')
@userapp.route('/user/<int:user_id>')
def profile(slug=None, user_id=None):
    return render_template('user/profile.html')

@userapp.route('/signou', methods=['GET'])
def signout():
    if 'user' in session:
        session.pop('user')
    return redirect('/')
