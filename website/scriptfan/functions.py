# -*- coding: utf-8 -*-
"""
    scriptfan.functions
    ~~~~~~~~~~~~~~~~~~~

    一些通用的工具方法，包括获取参数，md5等
"""

import hashlib
from functools import wraps
from urlparse import urlparse, urljoin

from flask import request, flash, redirect, url_for
from flask.ext.babel import gettext as _

from scriptfan import permissions

def md5(password):
    return hashlib.md5(password).hexdigest()


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and\
           ref_url.netloc == test_url.netloc

def get_page():
    """ 试图从请求参数中取出当前页码，如果失败，返回1 """

    try:
        return int(request.args.get('page', '1'))
    except ValueError:
        return 1

def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            return url_for('home.index')
        if is_safe_url(target):
            return target

def require_roles(*roles):
    for role_name in roles:
        if hasattr(permissions, role_name):
            print getattr(permissions, role_name)
            if getattr(permissions, role_name).can():
                return True

    return False


def roles_required(*roles):
    """
    此方法用于在 action 上建立权限验证，用法如下 ::

        @app.route('/some_action')
        @roles_required('admin', 'root')
        def some_action():
            return 'Foo'

    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if require_roles(*roles): 
                return f(*args, **kwargs)
            else:
                flash(_('messages.permission_denied'), 'error') 
                return redirect(get_redirect_target())

        return decorated_function
    return decorator
