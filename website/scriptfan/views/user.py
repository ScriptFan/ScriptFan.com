#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Blueprint, session, url_for, redirect, render_template, flash, current_app as app
from flask.ext import wtf, login
from scriptfan.extensions import db, login_manager
from scriptfan.models import get_user, User
userapp = Blueprint("user", __name__)

login_manager.login_view = 'login'
login_manager.login_view = u'需要登陆后才能访问本页'

class LoginUser(login.UserMixin):
    """Wraps User object for Flask-Login"""

    def __init__(self, user):
        self.id = user.id
        self.user = user 

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id) 
    return user and LoginUser(user) or None

class SigninForm(wtf.Form):
    email = wtf.TextField('email', validators=[
        wtf.Required(message=u'请填写电子邮件'), 
        wtf.Email(message=u'无效的电子邮件')])
    password = wtf.PasswordField('password', validators=[
        wtf.Required(message=u'请填写密码'),
        wtf.Length(min=5, max=20, message=u'密应应为5到20位字符')])
    next = wtf.HiddenField('next')
    remember = wtf.BooleanField('remember')

    def __init__(self, *args, **kargs):
        wtf.Form.__init__(self, *args, **kargs)
        self.user = None

    def validate(self):
        # 验证邮箱是否注册
        if wtf.Form.validate(self):
            user = get_user(email=self.email.data)
            if not user:
                self.email.errors.append(u'该邮箱尚未在本站注册')
            elif not user.check_password(self.password.data):
                self.password.errors.append(u'密码错误')
            else:
                self.user = user

        return len(self.errors) == 0

@userapp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm(csrf_enabled=False)
    userapp.info('>>> Signup user: ' + repr(dict(form.data, password='<MASK>')))
    if form.validate_on_submit():
        login.login_user(LoginUser(form.user), remember=form.remember)
        flash(u'登陆成功')
        # 如果指定了 next ，跳转到 next 页面
        # 如果用户注册了 slug ，则跳转到 slug  的profile 页面，否则跳转到 userid 的 profile 页面
        profile_context = form.user.slug and { 'slug': form.user.slug } or { 'user_id': form.user.id }
        return redirect(form.next.data or url_for('user.profile', **profile_context))
    else:
        return render_template('user/signin.html', form=form)

# @oid.after_login
# def create_or_login(resp):
#     session['openid'] = resp.identity_url
#     # user = get_user(openid=resp.identity_url)
#     user = None
#     if user is not None:
#         flash(u'成功登入')
#         session['user'] = str(user.id)
#         session.pop('openid')
#         # g.user = getUserObject(user_id=session['user'])
#         return redirect(oid.get_next_url())
#     return redirect(url_for('user.signup',
#                             next=oid.get_next_url(),
#                             nickname=resp.nickname,
#                             email=resp.email))

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
            user = get_user(email=self.email.data)
            user and self.email.errors.append(u'该邮箱已被注册')
        
        self.user = User(self.nickname.data, self.email.data)
        self.user.set_password(self.password.data)
        return len(self.errors) == 0

@userapp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(csrf_enabled=False)
    app.logger.info('>>> Signup user: ' + repr(dict(form.data, password='<MASK>')))
    app.logger.info('>>> Signup user: ' + repr(dict(form.data, password='<MASK>')))
    app.logger.info('>>> Signup user: ' + repr(dict(form.data, password='<MASK>')))
    app.logger.info('>>> Signup user: ' + repr(dict(form.data, password='<MASK>')))
    if form.validate_on_submit():
        db.session.add(form.user)
        db.session.commit()
        return redirect(url_for('user.signin'))
    else:
        return render_template('user/signup.html', form=form)

@userapp.route('/profile/<slug>')
@userapp.route('/profile/<int:user_id>')
def profile(slug=None, user_id=None):
    return render_template('user/profile.html')

@userapp.route('/signou', methods=['GET'])
def signout():
    if 'user' in session:
        session.pop('user')
    return redirect('/')
