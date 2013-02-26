#-*- coding: utf-8 -*-
"""
    scriptfan.forms.event
    ~~~~~~~~~~~~~~~~~~~~~~~
    Forms for events
"""

from flask.ext import wtf
from scriptfan.forms.base import RedirectForm
from datetime import date

class EventForm(RedirectForm):
    title = wtf.TextField(u'活动标题', validators=[ \
            wtf.Required(message=u'请为活动填写一个标题')])
    content = wtf.TextAreaField(u'活动简介', validators=[ \
            wtf.Length(min=10, max=5000, message=u'简介至少10个字')])
    date = wtf.TextField(u'活动日期', default=date.today,
            validators=[ wtf.Required(message=u'需要指定活动日期')])
    start_time = wtf.TextField(u'开始时间', default='13:30', validators=[ \
            wtf.Required(message=u'需要指定开始时间')])
    end_time = wtf.TextField(u'结束时间', default='17:00', validators=[ \
            wtf.Required(message=u'需要指定结束时间')])
    address = wtf.TextField(u'活动地点')
    latitude = wtf.HiddenField()
    longitude = wtf.HiddenField()
