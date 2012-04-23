#!/usr/bin/python
#-*-coding:utf-8-*-
from flaskext.mongoengine import MongoEngine
from flaskext.openid import OpenID

db = MongoEngine()
oid = OpenID()
