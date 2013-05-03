# -*- coding: utf-8 -*-
"""
    scriptfan.functions
    ~~~~~~~~~~~~~~~~~~~

    一些通用的工具方法，包括获取参数，md5等
"""

import hashlib
from urlparse import urlparse, urljoin
from flask import request
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
            continue
        if is_safe_url(target):
            return target

def require(*roles):
    for role_name in roles:
        if hasattr(permissions, role_name):
            print getattr(permissions, role_name)
            if getattr(permissions, role_name).require():
                return True

    return False
            
