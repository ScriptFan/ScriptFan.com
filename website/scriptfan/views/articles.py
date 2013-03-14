# -*- coding: utf-8 -*-
"""
    scriptfan.views.articles
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Views controllers for articles and categoirs
"""

from datetime import datetime

from flask import Blueprint, render_template, redirect, flash, url_for
from scriptfan import db
from scriptfan.forms.articles import ArticleForm
from scriptfan.models import Article, Category

from flask.ext.login import current_user


blueprint = Blueprint("articles", __name__)

@blueprint.route('/', methods=['GET'])
def index():
    articles = Article.query.all()
    return render_template('articles/index.html')

@blueprint.route('/create', methods=['GET', 'POST'])
def create():
    return 'Not implemented' 
