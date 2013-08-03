#-*- coding: utf-8 -*-

"""
    scriptfan/forms/articles
    ~~~~~~~~~~~~~~~~~~~~~~~~

    文章相关的表单
"""

from flask.ext import wtf
from scriptfan.forms.base import RedirectForm


class ArticleForm(RedirectForm):
    """ 文章发布和修改的表单 """

    title = wtf.TextField('title', validators=[wtf.Required(message=u'请填写标题')])
    content = wtf.TextAreaField('content', validators=[wtf.Required(message=u'文章内容不能为空')])
    tags_text = wtf.HiddenField('tags_text')
    published = wtf.BooleanField('published')
