#-*- coding: utf-8 -*-
from flaskext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

oid = OpenID()
db = SQLAlchemy()
login_manager = LoginManager()
