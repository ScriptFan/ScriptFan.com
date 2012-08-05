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
