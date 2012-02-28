#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Flask
from flask_peewee.db import Database

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("scriptfan.cfg")

    return app

def dispatch_apps(app):
    from scriptfan.views import news_modular, site_modular
    app.register_blueprint(news_modular)
    app.register_blueprint(site_modular)

app = create_app()
db = Database(app)

dispatch_apps(app)
