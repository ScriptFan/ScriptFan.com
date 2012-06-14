#!/usr/bin/env python
#-*-coding:utf-8-*-
from scriptfan.variables import db

__all__ = ["User", "UserInfo", "getUserObject"]

def getUserObject(slug=None, user_id=None):
    user = None
    if not slug and not user_id:
        if 'user' in session:
            user = g.user
    elif slug:
        user = User.query.filter_by(slug=slug).first()
    elif user_id:
        user = User.query.filter_by(id=user_id).first()
    return user

class UserInfo(db.Model):
    """
    用户信息表
    """
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    motoo = db.Column(db.String(255))
    introduction = db.Column(db.Text)

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return "<UserInfo (%s)>" % self.user_id

class User(db.Model):
    """
    用户表
    修改email地址时需要经过验证
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(45), unique=True, nullable=False) # 登陆使用的
    nickname = db.Column(db.String(45), unique=True, nullable=False) # 显示时用的
    password = db.Column(db.String(45), nullable=True)
    is_email_verified = db.Column(db.Boolean, nullable=False)
    slug = db.Column(db.String(45), nullable=True)
    created_time = db.Column(db.DateTime, nullable=False)
    modified_time = db.Column(db.DateTime, nullable=False)
    last_login_time = db.Column(db.DateTime, default=datetime.now())

    info = db.relationship('UserInfo', uselist=False)

    def __init__(self, nickname, email):
        self.nickname = nickname
        self.email = email
        self.paste_num = 0
        self.created_time = self.modified_time = datetime.now()
        self.is_email_verified = True

    def __repr__(self):
        return "<User (%s|%s)>" % (self.nickname, self.email)

    def set_password(self, password):
        self.password = hashPassword(password)

    @property
    def url(self):
        if self.slug:
            return url_for('userapp.view', slug=self.slug)
        return url_for('userapp.view', user_id=self.id)

    def get_avatar_url(self, size=20):
        return "http://www.gravatar.com/avatar/%s?size=%s&d=%s/static/images/avatar/default.jpg" % (
                hashlib.md5(self.email).hexdigest(),
                size,
                request.url_root)

class Activity(db.Model):
    pass
