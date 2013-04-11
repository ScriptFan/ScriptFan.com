#-*- coding: utf-8 -*-

"""
    scriptfan/forms/articles
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Forms for articles and categories
"""

from flask.ext import wtf
from scriptfan.forms.base import RedirectForm


class ArticleForm(RedirectForm):
    """ Form for article create and update """

    title = wtf.TextField('title', validators=[wtf.Required(message=u'请填写标题')])
    content = wtf.TextAreaField('content', validators=[wtf.Required(message=u'文章内容不能为空')])
