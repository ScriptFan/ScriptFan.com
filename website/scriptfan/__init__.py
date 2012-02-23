#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Flask
from flask_peewee.db import Database

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("scriptfan.cfg")

    from scriptfan.views import *
    app.register_blueprint(news_modular)
    app.register_blueprint(site_modular)

    return app

app = create_app()
db = Database(app)
