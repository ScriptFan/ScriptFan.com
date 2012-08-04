#!/usr/bin/env python
#-*-coding:utf-8-*-
import logging
from pprint import pformat
from flask import Blueprint, request, url_for, redirect, render_template, abort, flash, g
from flask.ext.wtf import Form, TextField, PasswordField, Required
from scriptfan.extensions import *
from scriptfan.models import User, UserInfo
userapp = Blueprint("user", __name__)

class LoginForm(Form):
    email = TextField('email', validators=[Required()])

@userapp.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    form = LoginForm(request.form, csrf_enabled=False)
    if request.method == 'POST':
        openid = request.form.get('openid', None)
        if openid:
            return oid.try_login(COMMON_PROVIDERS.get(openid, "fackeone"),
                                 ask_for=['email', 'nickname'])
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                user.last_login_time = datetime.now()
                session['user'] = str(user.id)
                return redirect(request.args.get('next', '/'))
    g.form = form
    return render_template('user/login.html',
                           next=oid.get_next_url(),
                           error=oid.fetch_error())

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
    return redirect(url_for('user.register',
                            next=oid.get_next_url(),
                            nickname=resp.nickname,
                            email=resp.email))

class RegisterForm(Form):
    email = TextField('email', validators=[Required()])
    nickname = TextField('nickname', validators=[Required()])
    password = PasswordField('password', validators=[Required()])

    def __init__(self, *args, **kargs):
        Form.__init__(self, *args, **kargs)
        self.user = None

    def validate(self):
        if not Form.validate(self):
            return False

        # 验证邮箱是否注册
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append(u'该邮箱已被注册')
            return False

        self.user = User(*self.data, info=UserInfo())
        return True

@userapp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(csrf_enabled=False)
    logging.info('>>> Register user: ' + repr(dict(form.data, password='<MASK>')))
    if form.validate_on_submit():
        db.session.add(form.user)
        db.session.commit()
        return redirect(url_for('userapp.login'))
    else:
        logging.info(form.errors)
        return render_template('user/register.html', next_url=oid.get_next_url(), form=form)

@userapp.route('/profile', methods=['GET'])
def profile():
    return render_template('user/profile.html')

@userapp.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect('/')
