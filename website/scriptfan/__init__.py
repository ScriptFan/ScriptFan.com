#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Flask

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    from scriptfan.views import *
    app.register_blueprint(news_modular)
    app.register_blueprint(site_modular)

    return app

