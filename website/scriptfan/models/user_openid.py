# -*- coding: utf-8 -*-
"""
    scriptfan.models.user_openid
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Model for table: user_openids
"""

from scriptfan import db

class UserOpenID(db.Model):
    """ 用户OpenID绑定表 """

    __tablename__ = 'user_openids'

    id = db.Column(db.Integer, primary_key=True)
    #: openid 关联的用户 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), \
                        nullable=False)
    #: openid 授权的值
    openid = db.Column(db.String(255), nullable=False, unique=True)
    #: opendid 提供商, 例如 google
    provider = db.Column(db.String(50), nullable=False)
