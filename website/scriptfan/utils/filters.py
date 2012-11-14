#!/usr/bin/env python
#-*-coding:utf-8-*-
from datetime import datetime


def dateformat(value, format="%Y-%m-%d %H:%M"):
    return value.strftime(format)


def empty(value, text=None):
    if not value:
        if text:
            return text
    return value


def error_class(filed):
    """ 用于显示 bootstrap 表单的 control-group 中添加 ``error`` 类
    如果表单字段中存在错误，则返回 error，否则返回空。
    """

    return filed.errors and 'error' or ''


def error_text(field, default='', sep='；'):
    """ 如果表单项中存在砥中，则显示错误，否则显示默认文本 """

    return field.errors and sep.join(field.errors) or default


def time_passed(value):
    now = datetime.now()
    past = now - value
    if past.days:
        return u'%s天前' % past.days
    mins = past.seconds / 60
    if mins < 60:
        return u'%s分钟前' % mins
    hours = mins / 60
    return u'%s小时前' % hours
