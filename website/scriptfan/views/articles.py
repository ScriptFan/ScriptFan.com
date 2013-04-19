# -*- coding: utf-8 -*-
"""
    scriptfan.views.articles
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Views controllers for articles and categoirs
"""

from flask import (Blueprint, render_template, redirect,
                   flash, url_for, request, current_app as app)
from flask.ext import login
from flask.ext.login import current_user
from flask.ext.babel import gettext as _

from scriptfan import db
from scriptfan.functions import get_page
from scriptfan.forms.articles import ArticleForm
from scriptfan.models import Article, Tag


blueprint = Blueprint("articles", __name__)


@blueprint.route('/', methods=['GET'])
def index():
    articles = Article.query.order_by('created_time DESC') \
                      .paginate(get_page(), app.config.get('PAGE_SIZE', 10))
    return render_template('articles/index.html', articles=articles)


@blueprint.route('/<int:article_id>', methods=['GET'])
def show(article_id):
    article = Article.query.get(article_id)
    return render_template('articles/show.html', article=article)


@blueprint.route('/create', methods=['GET', 'POST'])
@login.login_required
def create():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article()
        form.populate_obj(article)
        article.author_id = current_user.user.id
        db.session.add(article)
        db.session.commit()
        flash('Add article successfully!', 'success')
        return redirect(url_for('.show', article_id=article.id))

    return render_template('articles/new.html', form=form)


@blueprint.route('/edit/<int:article_id>', methods=['GET', 'POST'])
@login.login_required
def update(article_id):
    article = Article.query.get(article_id)
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.commit()
        flash('Update article successfully!', 'success')
        return redirect(url_for('.index'))

    app.logger.info(form.data)
    return render_template('articles/edit.html', form=form)
