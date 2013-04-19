# -*-coding: utf-8-*-
"""
    scriptfan.models.articles
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    文章及相关表对应的模型及事件绑定
"""

from flask import current_app as app
from datetime import datetime
from sqlalchemy import event

from scriptfan import db
from scriptfan.filters import markdown


# 文章对应标签的映射
article_tags = db.Table('article_tags',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    content_html = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_time = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now)

    tags = db.relationship('Tag', secondary=article_tags, backref=db.backref('articles', lazy='dynamic'))

    @property
    def tags_text(self):
        return ','.join([tag.name for tag in self.tags])

    @tags_text.setter
    def tags_text(self, value):
        # 仅当 tags 发生变化时才进行重新分配
        if value != self.tags_text:
            if self.id:
                self.tags.delete()
            
            for tag_name in value.split(','):
                tag = Tag.query.filter_by(name=tag_name).first() or Tag(name=tag_name)
                self.tags.append(tag)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    count = db.Column(db.Integer, default=0)

def article_content_changed(article, content, old_content, initiator):
    """ 如果文章的正文变更，重新通过markdown转换html """

    # `markdown2.markdown` 返回的结果是 `UnicodeWithAttrs` 是 unicode 的一个子类
    # 包含了一些 markdown 的专有结果，比如 toc ，sqlalchemy 无法识别，所以这里需要转换一层
    article.content_html = unicode(markdown(content))

event.listen(Article.content, 'set', article_content_changed)

