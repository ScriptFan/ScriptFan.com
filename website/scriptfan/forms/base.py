# -*- coding: utf-8 -*-
"""
    scriptfan.forms.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    Base redirect form
"""

from flask import url_for, redirect
from scriptfan.functions import get_redirect_target, is_safe_url
from flask.ext.wtf import Form, HiddenField

class RedirectForm(Form):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))