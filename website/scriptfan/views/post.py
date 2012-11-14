#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Blueprint, render_template, g
from scriptfan.models import *

postapp = Blueprint("post", __name__, url_prefix="/post")

@postapp.route('/')
def index():
    g.posts = Post.objects.all()
    return render_template('post/index.html')
