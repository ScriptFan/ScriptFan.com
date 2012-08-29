#-*- coding: utf-8 -*-
from flaskext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

__all__ = [ 'oid', 'db', 'login_manager']

oid = OpenID()
db = SQLAlchemy()
login_manager = LoginManager()
