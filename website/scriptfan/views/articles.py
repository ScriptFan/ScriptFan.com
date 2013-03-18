# -*- coding: utf-8 -*-
"""
    scriptfan.views.articles
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Views controllers for articles and categoirs
"""

from flask import (Blueprint, render_template, redirect,
                   flash, url_for, request, current_app as app)
from flask.ext.login import current_user
from flask.ext.babel import gettext as _

from scriptfan import db
from scriptfan.forms.articles import ArticleForm
from scriptfan.models import Article, Category


blueprint = Blueprint("articles", __name__)


@blueprint.route('/', methods=['GET'])
def index():
    articles = Article.query.all()
    # app.logger.info(articles[0].title)
    return render_template('articles/index.html',
                            articles=articles)

@blueprint.route('/<int:article_id>', methods=['GET'])
def show(article_id):
    article = Article.get_by_id(article_id)
    return render_template('articles/show.html', article=article)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
    title = _("articles.create")
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article()
        form.populate_obj(article)
        db.session.add(article)
        db.session.commit()
        flash('Add article successfully!', 'success')
        return redirect(url_for('.show', article_id=article.id))

    return render_template('articles/new.html', form=form)


@blueprint.route('/edit/<int:article_id>', methods=['GET', 'POST'])
def update(article_id):
    title = _("articles.update")
    article = Article.get_by_id(article_id)
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.commit()
        flash('Update article successfully!', 'success')
        return redirect(url_for('.show', article_id=article.id))

    return render_template('articles/edit.html', form=form)
