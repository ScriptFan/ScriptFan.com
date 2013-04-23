# -*- coding: utf-8 -*-
"""
    scriptfan.permissions
    ~~~~~~~~~~~~~~~~~~~~~~
    scriptfan 的权限定义
    1-被封用户 2-保留用户 3-普通用户 4-普通管理员 5-超级管理员
"""

from flask.ext.principal import RoleNeed, Permission

banned  = Permission(RoleNeed(1))
suspend = Permission(RoleNeed(2))
user    = Permission(RoleNeed(3))
admin   = Permission(RoleNeed(4))
root    = Permission(RoleNeed(5))

