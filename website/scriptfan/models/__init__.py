# -*-coding: utf-8-*-
"""
    scriptfan.models
    ~~~~~~~~~~~~~~~~~~

    Model package for scriptfan
"""

from .user import User
from .user_openid import UserOpenID
from .event import Event

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
#     user = db.relationship(User, backref='topics', lazy='dynamic')

# 用户参与活动的跟踪表
# activity_users = db.Table('activity_users',
#     db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True),
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
# )
# 
# # 活动相关资源
# activity_resources = db.Table('activity_resources',
#     db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True),
#     db.Column('resource_id', db.Integer, db.ForeignKey('resources.id'), primary_key=True),
# )


#  
# class ActivityComment(db.Model):
#     """
#     活动评论表
#     如果是未注册用户使用openid注册，则仅将openid记录在cookie中
#     """
#     __tablename__ = 'activity_comments'
# 
#     id = db.Column(db.Integer, primary_key=True)
#     author_name = db.Column(db.String(50), nullable=False) # 作者昵称
#     author_email = db.Column(db.String(255)) # 作者邮件地址
#     author_site = db.Column(db.String(255)) # 作者网址
#     content = db.Column(db.Text, nullable=False) # 评论内容
#     created_time = db.Column(db.DateTime) # 创建日期
#     modified_time = db.Column(db.DateTime) # 更新日期
#     
#     parent_id = db.Column(db.Integer, db.ForeignKey('activity_comments.id'), nullable=True)
#     children = db.relationship('ActivityComment', backref='parent', remote_side=[id]) # 回复评论的引用
#     
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     user = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))
