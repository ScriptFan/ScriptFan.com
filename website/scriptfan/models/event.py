# -*-coding: utf-8-*-
"""
    scriptfan.models.event
    ~~~~~~~~~~~~~~~~~~~~~~

    Model for table: events
"""

from scriptfan import db

class Event(db.Model):
    """
    活动表
    每期活动需要一个公告
    """
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 发起人
    title = db.Column(db.String(255)) # 活动标题
    content = db.Column(db.Text) # 活动介绍
    content_html = db.Column(db.Text) # 转换后的省劲介绍内容
    address = db.Column(db.String(255)) # 活动地址
    lat = db.Column(db.Numeric(10, 7)) # 纬度
    lng = db.Column(db.Numeric(10, 7)) # 经度
    created_time = db.Column(db.DateTime) # 活动创建时间
    updated_time = db.Column(db.DateTime) # 活动更新时间

    durations = db.relationship('EventDuration', backref=db.backref('event'))

    followers = db.relationship('User', secondary='event_members',
            backref=db.backref('events', lazy='dynamic')) # 参与者
    resources = db.relationship('Resource', secondary='event_resources',
            backref=db.backref('events', lazy='dynamic')) # 话题相关资源


# 用户参与活动的跟踪表
event_members = db.Table('event_members',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'),
              primary_key=True),
    db.Column('member_id', db.Integer, db.ForeignKey('users.id'),
              primary_key=True),
)


# 活动相关资源
event_resources = db.Table('event_resources',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'),
              primary_key=True),
    db.Column('resource_id', db.Integer, db.ForeignKey('resources.id'),
              primary_key=True),
)