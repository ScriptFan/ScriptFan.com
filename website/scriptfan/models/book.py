# -*-coding: utf-8-*-
"""
    scriptfan.models.articles
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Model for table: articles
"""

from scriptfan import db
from datetime import datetime


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=True)
    isbn = db.Column(db.String(255), nullable=True)
    created_time = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class BookRecord(db.Model):
    __tablename__ = 'book_record'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.relationship('User', backref=db.backref('users'))
    book_id = db.relationship('Book', backref=db.backref('books'))
    created_time = db.Column(db.DateTime, default=datetime.now)
    return_time = db.Column(db.DateTime, default=datetime.now)
