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
