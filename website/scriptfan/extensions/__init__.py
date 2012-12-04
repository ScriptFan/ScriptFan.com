#-*- coding: utf-8 -*-
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.babel import Babel

__all__ = ['oid', 'db', 'login_manager', 'babel']

oid = OpenID()
db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()
