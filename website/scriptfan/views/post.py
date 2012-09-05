#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Blueprint, render_template, g
from scriptfan.models import *

postmodular = Blueprint("post", __name__, url_prefix="/post")

@postmodular.route('/')
def index():
    g.posts = Post.objects.all()
    return render_template('post/index.html')
