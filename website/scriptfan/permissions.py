# -*- coding: utf-8 -*-
"""
    scriptfan.permissions
    ~~~~~~~~~~~~~~~~~~~~~~
    scriptfan 的权限定义
    1-被封用户 2-保留用户 3-普通用户 4-普通管理员 5-超级管理员
"""

from flask.ext.principal import RoleNeed, Permission

banned  = Permission(RoleNeed(u'1'))
suspend = Permission(RoleNeed(u'2'))
user    = Permission(RoleNeed(u'3'))
admin   = Permission(RoleNeed(u'4'))
root    = Permission(RoleNeed(u'5'))

