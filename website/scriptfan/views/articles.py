# -*- coding: utf-8 -*-
"""
    scriptfan.views.articles
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Views controllers for articles and categoirs
"""

from flask import (Blueprint, render_template, redirect,
                   flash, url_for, request)
from flask.ext.login import current_user

from scriptfan import db
from scriptfan.forms.articles import ArticleForm
from scriptfan.models import Article, Category


blueprint = Blueprint("articles", __name__)


@blueprint.route('/', methods=['GET'])
def index():
    articles = Article.query.all()
    return render_template('articles/index.html',
                            articles=articles)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        article = Article(title=form.title.data,
                          content=form.content.data)
        db.session.add(article)
        db.session.commit()
        flash('Add article successfully!')
        return redirect(url_for('.create'))
    return render_template('articles/create.html', form=form)
