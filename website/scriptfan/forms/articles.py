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

    title = wtf.TextField('email', validators=[wtf.Required(message=u'请填写标题')])
    content = wtf.TextAreaField('content', validators=[wtf.Required(message=u'文章内容不能为空')])
    # TODO: Fill article category dropdown with categories
    category_id = wtf.SelectField('category_id')

class CategoryForm(RedirectForm):
    """ Form for category create and update """

    # TODO: Add unique validations for name and slug
    name = wtf.TextField("name", validators=[wtf.Required(message=u'名称不能为空')])
    slug = wtf.TextField("slug", validators=[wtf.Required(message=u'名称不能为空')])
