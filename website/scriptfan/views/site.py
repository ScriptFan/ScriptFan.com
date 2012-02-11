#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Blueprint, render_template

site_modular = Blueprint("site", __name__, url_prefix="/")

@site_modular.route("/")
def index():
    return render_template("site/index.html")
