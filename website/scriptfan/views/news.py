#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Blueprint, render_template, g
from scriptfan.models import *

news_modular = Blueprint("news", __name__, url_prefix="/news")

@news_modular.route('/')
def index():
    g.news = News.select().order_by('created_time DESC')
    return render_template('news/index.html')
