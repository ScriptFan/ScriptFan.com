#!/usr/bin/env python
#-*-coding:utf-8-*-
from datetime import datetime
from hashlib import md5, sha1
from flask_peewee.auth import BaseUser
from peewee import *
from scriptfan import db

__all__ = ["User", "Relationship", "News", "NewsComment"]

class User(db.Model, BaseUser):
    nickname = CharField()
    password = CharField()
    email = CharField()
    created_time = DateTimeField(default=datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.nickname

    def following(self):
        return User.select().join(
            Relationship, on='to_user_id'
        ).where(from_user=self).order_by('nickname')

    def followers(self):
        return User.select().join(
            Relationship
        ).where(to_user=self).order_by('nickname')

    def is_following(self, user):
        return Relationship.filter(
            from_user=self,
            to_user=user
        ).exists()

    def gravatar_url(self, size=80):
        return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
            (md5(self.email.strip().lower().encode('utf-8')).hexdigest(), size)

class Relationship(db.Model):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')

    def __unicode__(self):
        return 'Relationship from %s to %s' % (self.from_user, self.to_user)

class News(db.Model):
    user = ForeignKeyField(User)
    title = CharField()
    content = TextField()
    created_time = DateTimeField(default=datetime.now())
    modified_time = DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.title

class NewsComment(db.Model):
    news = ForeignKeyField(News)
    user = ForeignKeyField(User)
    content = TextField()
    created_time = DateTimeField(default=datetime.now())
    modified_time = DateTimeField(default=datetime.now())

    def __unicode__(self):
        return "%s@%s" % (self.user.nickname, self.title)

