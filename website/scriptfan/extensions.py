#!/usr/bin/python
#-*-coding:utf-8-*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.openid import OpenID

app = Flask(__name__)
db = SQLAlchemy()
oid = OpenID()
