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
from scriptfan.functions import get_page, roles_required, require_roles
from scriptfan.forms.base import RedirectForm
from scriptfan.forms.articles import ArticleForm
from scriptfan.models import Article, Tag
from scriptfan import permissions

blueprint = Blueprint("articles", __name__)


@blueprint.route('/', methods=['GET'])
@blueprint.route('/tag/<tag_name>/', methods=['GET'])
def index(tag_name=None):
    articles = Article.query

    # 对于非管理员，只能看到发布过的文章
    if not require_roles('admin', 'root'):
        articles = articles.filter_by(published=1)

    if tag_name:
        articles = articles.filter(Article.tags.any(name=tag_name))

    articles = articles.order_by('created_time DESC').paginate(get_page(), app.config.get('PAGE_SIZE', 10))
    tags = Tag.query.all()
    return render_template('articles/index.html', articles=articles, tags=tags, tag_name=tag_name)


@blueprint.route('/<int:article_id>/', methods=['GET'])
def show(article_id):
    article = Article.query.get(article_id)
    tags = Tag.query.all()
    destroy_form = RedirectForm()
    return render_template('articles/show.html', article=article, tags=tags, destroy_form=destroy_form)


@blueprint.route('/create/', methods=['GET', 'POST'])
@roles_required('admin', 'root')
@login.login_required
def create():
    form = ArticleForm()
    if form.validate_on_submit():
        app.logger.info('Create new article %s', form.title.data)
        article = Article()
        form.populate_obj(article)
        app.logger.info('  Tagged as %s', form.tags_text.data)
        article.author_id = current_user.user.id
        db.session.add(article)
        db.session.commit()
        flash('Add article successfully!', 'success')
        return redirect(url_for('.show', article_id=article.id))

    tags = Tag.query.all()
    return render_template('articles/new.html', form=form, tags=tags)


@blueprint.route('/edit/<int:article_id>/', methods=['GET', 'POST'])
@roles_required('admin', 'root')
@login.login_required
def update(article_id):
    article = Article.query.get(article_id)
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        app.logger.info('Updating article: #%s %s', article.id, article.title)
        app.logger.info('  Old tags: %s', article.tags_text)
        form.populate_obj(article)
        app.logger.info('  New tags: %s', article.tags_text)
        db.session.commit()
        flash('Update article successfully!', 'success')
        return redirect(url_for('.index'))

    tags = Tag.query.all()
    return render_template('articles/edit.html', form=form, tags=tags)

@blueprint.route('/<int:article_id>/destroy/', methods=['POST'])
@roles_required('admin', 'root')
def destroy(article_id):
    article = Article.query.get(article_id)
    flash('Destroy article successfully!', 'success')
    db.session.delete(article)
    return redirect(url_for('.index'))

