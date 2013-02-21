from scriptfan import db

# -*-coding: utf-8-*-
"""
    scriptfan.models.resource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Model for table: resources
"""

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
