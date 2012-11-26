#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import request, url_for
from datetime import datetime
from scriptfan.extensions import db
from scriptfan.utils.functions import md5

def get_user(slug=None, user_id=None, email=None):
    user = None
    
    if email:
        user = User.query.filter_by(email=email).first()
    elif slug:
        user = User.query.filter_by(slug=slug).first()
    elif user_id:
        user = User.query.filter_by(id=user_id).first()

    return user

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
        return "<User (%s|%s)>" % (self.nickname, self.email)

    def set_password(self, password):
        self.password = md5(password)

    def check_password(self, password):
        return self.password == md5(password)

    @property
    def url(self):
        if self.slug:
            return url_for('user.profile', slug=self.slug)
        return url_for('user.profile', user_id=self.id)

    def get_avatar_url(self, size=20):
        url_tpl = 'http://www.gravatar.com/avatar/%s?size=%s&d=%s%s'
        return url_tpl % (md5(self.email), size, request.url_root, url_for('static', filename='images/avatars/default.png'))

class UserOpenID(db.Model):
    """ OpenID绑定表 """
    __tablename__ = 'user_openids'

    id = db.Column(db.Integer, primary_key=True)
    #: openid 关联的用户 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    #: openid 授权的值
    openid = db.Column(db.String(255), nullable=False, unique=True)
    #: opendid 提供商, 例如 google
    provider = db.Column(db.String(50), nullable=False)

class Resource(db.Model): 
    """
    资源表
    汇集图片、视频、演示文稿等资源, 用于嵌入活动中
    """
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 发布者
    filetype = db.Column(db.String(50)) # 类型: video, audio, image, slides, pdf, webpage, ...
    url = db.Column(db.String(255)) # 资源地址，可以是外部地址，也可以是内部地址
    created_time = db.Column(db.DateTime)
    modified_time = db.Column(db.DateTime)

# 活动相关资源
topic_resources = db.Table('topic_resources',
    db.Column('topic_id', db.Integer, db.ForeignKey('topics.id'), primary_key=True),
    db.Column('resource_id', db.Integer, db.ForeignKey('resources.id'), primary_key=True),
)

# 用户参与投票的跟踪表（活动关闭后可清除此表数据）
topic_users = db.Table('topic_users',
    db.Column('topic_id', db.Integer, db.ForeignKey('topics.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
)

class Topic(db.Model):
    """
    活动的话题
    """
    __tablename__ = 'topics'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255)) # 话题名称
    inro = db.Column(db.Text) # 简要介绍
    rate_count = db.Column(db.Integer, default=0) # 投票数
    followers = db.relationship(User, secondary=topic_users) # 参与者
    resources = db.relationship(Resource, secondary=topic_resources) # 话题相关资源

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(User, backref='topics', lazy='dynamic')

# 用户参与活动的跟踪表
activity_users = db.Table('activity_users',
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
)

# 活动相关资源
activity_resources = db.Table('activity_resources',
    db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True),
    db.Column('resource_id', db.Integer, db.ForeignKey('resources.id'), primary_key=True),
)


class Activity(db.Model):
    """
    活动表
    每期活动需要一个公告
    """
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 发起人
    title = db.Column(db.String(255)) # 活动标题
    content = db.Column(db.Text) # 活动介绍
    slug = db.Column(db.String(255)) # 页面地址
    start_time = db.Column(db.DateTime) # 活动开始时间
    end_time = db.Column(db.DateTime) # 活动结束时间
    address = db.Column(db.String(255)) # 活动地址
    longitude = db.Column(db.Numeric(10, 7)) # 经度
    latitude = db.Column(db.Numeric(10, 7)) # 纬度
    created_time = db.Column(db.DateTime) # 活动创建时间
    modified_time = db.Column(db.DateTime) # 活动更新时间

    followers = db.relationship(User, secondary=activity_users, 
            backref=db.backref('activities', lazy='dynamic')) # 参与者
    resources = db.relationship(Resource, secondary=activity_resources, 
            backref=db.backref('activities', lazy='dynamic')) # 话题相关资源
 
class ActivityComment(db.Model):
    """
    活动评论表
    如果是未注册用户使用openid注册，则仅将openid记录在cookie中
    """
    __tablename__ = 'activity_comments'

    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(50), nullable=False) # 作者昵称
    author_email = db.Column(db.String(255)) # 作者邮件地址
    author_site = db.Column(db.String(255)) # 作者网址
    content = db.Column(db.Text, nullable=False) # 评论内容
    created_time = db.Column(db.DateTime) # 创建日期
    modified_time = db.Column(db.DateTime) # 更新日期
    
    parent_id = db.Column(db.Integer, db.ForeignKey('activity_comments.id'), nullable=True)
    children = db.relationship('ActivityComment', backref='parent', remote_side=[id]) # 回复评论的引用
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))
