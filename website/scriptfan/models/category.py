# -*-coding: utf-8-*-
"""
    scriptfan.models.category
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Model for table: categories
"""

from scriptfan import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    slug = db.Column(db.String(255), nullable=False, unique=True)

    articles = db.relationship('Article', backref=db.backref('category'))
