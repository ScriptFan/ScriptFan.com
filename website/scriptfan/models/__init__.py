# -*-coding: utf-8-*-
"""
    scriptfan.models
    ~~~~~~~~~~~~~~~~~~

    Model package for scriptfan
"""

from .user import User
from .user_openid import UserOpenID
from .event import Event
from .event_duration import EventDuration
from .resource import Resource
from .article import Article
from .category import Category

# 活动相关资源
# topic_resources = db.Table('topic_resources',
#     db.Column('topic_id', db.Integer, db.ForeignKey('topics.id'), primary_key=True),
#     db.Column('resource_id', db.Integer, db.ForeignKey('resources.id'), primary_key=True),
# )

# 用户参与投票的跟踪表（活动关闭后可清除此表数据）
# topic_users = db.Table('topic_users',
#     db.Column('topic_id', db.Integer, db.ForeignKey('topics.id'), primary_key=True),
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
# )

# class Topic(db.Model):
#     """
#     活动的话题
#     """
#     __tablename__ = 'topics'
#     
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255)) # 话题名称
#     inro = db.Column(db.Text) # 简要介绍
#     rate_count = db.Column(db.Integer, default=0) # 投票数
#     followers = db.relationship(User, secondary=topic_users) # 参与者
#     resources = db.relationship(Resource, secondary=topic_resources) # 话题相关资源
# 
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     users = db.relationship(User, backref='topics', lazy='dynamic')
