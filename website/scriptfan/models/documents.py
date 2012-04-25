#!/usr/bin/env python
#-*-coding:utf-8-*-
from datetime import datetime
from flask import url_for, session, g
from scriptfan.variables import db
from scriptfan.utils.functions import *

__all__ = ['User', 'Tag', 'Entry', 'EntryComment', 'getUserObject', 'updateTags']

def updateTags(model, tags=[]):
    old_tags = [tag.name for tag in model.tags]
    tags_to_add = set(tags) - set(old_tags)
    tags_to_del = set(old_tags) - set(tags)
    for tag in tags_to_add:
        t = Tag.objects(name='%s' % tag.strip().lower()).first()
        if not t:
            t = Tag(name=tag.strip("'\", ").lower().replace(",", '').replace("_", '-'))
            t.save()
        else:
            t.times = t.times + 1
            t.save()
        model.tags.append(t)
    for tag in tags_to_del:
        t = Tag.objects(name='%s' % tag.strip().lower()).first()
        if t:
            model.tags.remove(t)
            t.times = t.times - 1
            t.save()
    model.save()

def getUserObject(slug=None, user_id=None):
    if not slug and not user_id:
        if 'user' in session:
            user = g.user
        else:
            user = User.objects(email='user@daimaduan.com').first()
    elif slug:
        user = User.objects(slug=slug).first()
    elif user_id:
        user = User.objects(id=user_id).first()
    return user

class UserInfo(db.EmbeddedDocument):
    motoo = db.StringField()
    introduction = db.StringField()

class User(db.Document):
    """docstring for User"""
    openid = db.StringField(required=False)
    nickname = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=False)
    slug = db.StringField(default='')
    paste_num = db.IntField(default=0)
    created_time = db.DateTimeField(default=datetime.now())
    modified_time = db.DateTimeField(default=datetime.now())

    meta = {
        'ordering': ['nickname']
    }

    info = db.EmbeddedDocumentField(UserInfo)
    followers = db.ListField(db.ReferenceField('User'))
    favorites = db.ListField(db.ReferenceField('Paste'))

    def save(self, *args, **kwargs):
        if not self.info:
            self.info = UserInfo()
        super(User, self).save(*args, **kwargs)

    @property
    def url(self):
        if self.slug:
            return url_for('userapp.view', slug=user.slug)
        else:
            return url_for('userapp.view', user_id=self.id)

    def get_avatar_url(self, size=20):
        return "http://www.gravatar.com/avatar/%s?size=%s" % (hashlib.md5(self.url).hexdigest(), size)

    def get_user_dict(self):
        return {'id':user.id,
                'email':user.email,
                'nickname':user.nickname,
                'avatar':user.avatar}

class Tag(db.Document):
    name = db.StringField(required=True, unique=True)
    description = db.StringField()
    times = db.IntField(default=0)
    created_time = db.DateTimeField(default=datetime.now())
    modified_time = db.DateTimeField(default=datetime.now())

    meta = {
        'ordering': ['name']
    }

    followers = db.ListField(db.ReferenceField(User))

    @property
    def entries(self):
        return Entry.objects(tags=self)

class EntryComment(db.EmbeddedDocument):
    """docstring for Comment"""
    user = db.ReferenceField(User)
    content = db.StringField(required=True)
    created_time = db.DateTimeField(default=datetime.now())
    modified_time = db.DateTimeField(default=datetime.now())

    meta = {
        'ordering': ['-created_time']
    }

class Entry(db.Document):
    """docstring for Paste"""
    user = db.ReferenceField(User)
    syntax = db.ReferenceField(Syntax)
    title = db.StringField(default=u'未命名标题')
    content = db.StringField(required=True)
    description = db.StringField(default=u'没有描述')
    view_num = db.IntField(default=0)
    rate_num = db.IntField(default=0)
    created_time = db.DateTimeField(default=datetime.now())
    modified_time = db.DateTimeField(default=datetime.now())

    meta = {
        'ordering': ['-created_time']
    }

    comments = db.ListField(db.EmbeddedDocumentField(PasteComment))
    rates = db.ListField(db.EmbeddedDocumentField(PasteRate))
    tags = db.ListField(db.ReferenceField(Tag))
    followers = db.ListField(db.ReferenceField(User))

    def save(self, *args, **kwargs):
        if not self.id:
            self.followers.append(self.user)
        super(Paste, self).save(*args, **kwargs)

    def get_related_pastes(self, num):
        return Paste.objects(db.Q(syntax=self.syntax) & db.Q(id__ne=self.id))[:num]

    @property
    def is_user_followed(self):
        if g.user:
            return g.user in self.followers
        return False

    @property
    def is_user_favorited(self):
        if g.user:
            return self in g.user.favorites
        return False

