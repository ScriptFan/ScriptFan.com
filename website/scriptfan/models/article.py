# -*-coding: utf-8-*-
"""
    scriptfan.models.articles
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Model for table: articles
"""

from scriptfan import db
from datetime import datetime

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    #: Parsed html content
    content_html = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_time = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
