# -*-coding: utf-8-*-
"""
    scriptfan.models.user
    ~~~~~~~~~~~~~~~~~~~~~~

    Model for table: users
"""

from scriptfan import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    #: 用户页面的地址后缀，比如 http://scriptfan.com/profile/greatghoul 中的 greatghoul
    # 如果要填写，不能重复，因为 slug 要能够唯一标识一个用户 
    slug = db.Column(db.String(255), unique=True)
    #: 用户的昵称，昵称只是用户的称呼，可能重复
    nickname = db.Column(db.String(255), unique=True, nullable=False)
    #: 用户的密码（经过MD5加密的）
    password = db.Column(db.String(255))
    #: 邮件地址，可以不填，如果填写，不能重复
    email = db.Column(db.String(255), unique=True)
    #: 邮件的隐私度，0为不公开，1为对会员公司，2为完全公开
    email_privacy = db.Column(db.Integer, default=0)
    #: 用户的联系电话，可以不填写, 但如果填写的话，不能重复
    phone = db.Column(db.String(255), unique=True)
    #: 电话的隐私度，参考 `email_privacy`
    phone_privacy = db.Column(db.Integer, default=0)
    #: 用户的照片，考虑到是线下社区，所以留张照片能够方便大家互相认识，可以不上传
    photo = db.Column(db.String(255))
    #: 照片的隐私度，参考 `email_privacy`
    photo_privacy = db.Column(db.Integer, default=0)
    #: 一句话的座右铭
    motoo = db.Column(db.String(255))
    #: 用户的自己介绍，会通过 markdown 转换成 html 文本
    intro = db.Column(db.Text)
    #: 上次登陆的时间
    login_time = db.Column(db.DateTime)
    #: 注册时间
    created_time = db.Column(db.DateTime, default=datetime.now)
    #: 上次更新资料的时间
    updated_time = db.Column(db.DateTime, default=datetime.now)
    #: 简单的权限控制，控制级别：3-普通用户 4-管理员 (目前就这么简单，后面再讨论）
    privilege = db.Column(db.Integer, default=3)
  
    #: 用户 openid 的绑定列表
    openids = db.relationship('UserOpenID', backref=db.backref('user'))
    
    def __repr__(self):
        return u'<User (%s|%s)>' % (self.nickname, self.email)

    # 增加一段扰乱信息，这样更难破解
    def set_password(self, password):
        self.password = md5(password + app.config['PASSWORD_SALT'])

    def check_password(self, password):
        return self.password == md5(password + app.config['PASSWORD_SALT'])

    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()

    @classmethod
    def get_by_slug(cls, slug):
        return User.query.filter_by(slug=slug).first()

    @property
    def url(self):
        if self.slug:
            return url_for('user.profile', slug=self.slug)
        return url_for('user.profile', user_id=self.id)

    def get_avatar_url(self, size=20):
        url_tpl = 'http://www.gravatar.com/avatar/%s?size=%s&d=%s%s'
        return url_tpl % (md5(self.email), size, request.url_root, url_for('static', filename='images/avatars/default.png'))
