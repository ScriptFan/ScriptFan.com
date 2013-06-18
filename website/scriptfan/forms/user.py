#-*- coding: utf-8 -*-

"""
    scriptfan/forms/users.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    定义用户相关页面所用到的表单, 包括注册、登陆、基本资料修改、密码修改、邮箱修改等。
"""

from flask.ext import wtf
from flask.ext.login import current_user
from scriptfan.models import User
from scriptfan.forms.base import RedirectForm
from flask.ext.openid import COMMON_PROVIDERS

class SigninForm(RedirectForm):
    email = wtf.TextField('email', validators=[
        wtf.Required(message=u'请填写电子邮件'),
        wtf.Email(message=u'无效的电子邮件')])
    password = wtf.PasswordField('password', validators=[
        wtf.Required(message=u'请填写密码')])
    remember = wtf.BooleanField('remember')

    def validate(self):
        if not super(RedirectForm, self).validate(): return False

        user = User.get_by_email(self.email.data)
        if not user:
            self.email.errors.append(u'该邮箱未注册') 
        elif not user.check_password(self.password.data):
            self.password.errors.append(u'密码错误')
        else:
            self.user = user
        
        return not self.errors

class ResetStep1Form(RedirectForm):
    """请求发送密码重置邮件的表单"""

    email = wtf.TextField('email', validators=[
        wtf.Required(message=u'请填写电子邮件'),
        wtf.Email(message=u'无效的电子邮件')])
    # captcha = wtf.TextField('captcha', validators=[
    #     wtf.Required(message=u'请填写验证码')])

    def validate_email(form, field):
        form.user = User.get_by_email(field.data)
        if not form.user:
            raise wtf.ValidationError(u'该邮件尚未在本站注册') 


class ResetStep2Form(RedirectForm):
    """ 接收密码重置邮件后重新填写密码 """

    password = wtf.PasswordField(u'新密码', validators=[
        wtf.Required(message=u'请填写新密码，不能少与5位字符'),
        wtf.Length(min=5, max=20, message=u'密码应为5到20位字符')])
    confirm = wtf.PasswordField(u'确认密码', validators=[
        wtf.Required(message=u'请再次输入新密码'),
        wtf.EqualTo('password', message=u'两次输入的密码不一致')])


class SignupForm(RedirectForm):
    email = wtf.TextField('email', validators=[
        wtf.Required(message=u'请填写电子邮件'),
        wtf.Email(message=u'无效的电子邮件')])
    nickname = wtf.TextField('nickname', validators=[
        wtf.Required(message=u'请填写昵称')])
    password1 = wtf.PasswordField('password1', validators=[
        wtf.Required(message=u'请填写密码')])
    password2 = wtf.PasswordField('password2', validators=[
        wtf.Required(message=u'再次填写密码'),
        wtf.EqualTo('password1', message=u'两次输入的密码不一致')])

    def validate_email(form, field):
        if User.get_by_email(field.data):
            raise wtf.ValidationError(u'该邮箱已被注册') 


class EditProfileForm(RedirectForm):
    nickname = wtf.TextField('nickname', validators=[
        wtf.Required(message=u'请填写昵称')])
    phone = wtf.TextField('phone', validators=[
        wtf.Regexp(regex=r'^(1\d{10})?$', message=u'请输入有效的手机号码')])
    phone_privacy = wtf.RadioField('phone_privacy', choices=[
        ('0', u'不公开'), ('1', u'公开'), ('2', u'仅向会员公开')], default='0')
    # photo = db.Column(db.String(255), nullable=True) # 存一张照片，既然有线下的聚会的，总得认得人才行
    motoo = wtf.TextAreaField('motoo', validators=[
        wtf.Length(min=0, max=255, message=u'座右铭最多为255个字符')])
    intro = wtf.TextAreaField('introduction', validators=[
        wtf.Length(min=0, max=3000, message=u'个人介绍最多为3000个字')])


class EditPasswordForm(RedirectForm):
    old_password = wtf.PasswordField(u'当前密码', validators=[])
        #wtf.Required(message=u'请提供当前密码')])
    password = wtf.PasswordField(u'新密码', validators=[
        wtf.Required(message=u'请填写新密码，不能少与5位字符'),
        wtf.Length(min=5, max=20, message=u'密码应为5到20位字符')])
    confirm = wtf.PasswordField(u'确认密码', validators=[
        wtf.Required(message=u'请再次输入新密码'),
        wtf.EqualTo('password', message=u'两次输入的密码不一致')])

    def validate_old_password(form, field):
        # FIXME: 当用户密码为空时，跳过原始密码验证，是否存在安全隐患？
        if current_user.user.password and (not current_user.user.check_password(field.data)):
            raise wtf.ValidationError(u'提供的原始密码不正确')


class EditSlugForm(RedirectForm):
    # FIXME: 验证 slug 是否已经被占用
    slug = wtf.TextField('slug', validators=[
        wtf.Regexp(regex=r'^([a-zA-Z][a-zA-Z0-9_-]{4,23})?$', 
            message=u'长度应为5~24位，仅能包含数字、英文字母及下划线(_)和减号(-)，并且需要以字母开头')])


class ManageOpenIDForm(RedirectForm):
    method = wtf.HiddenField('method', validators=[
        wtf.AnyOf(['add', 'delete'], message=u'不支持该操作'), ])
    provider = wtf.HiddenField('provider', validators=[
        wtf.AnyOf(COMMON_PROVIDERS, message=u'还不能绑定到该OpenID'), ])


