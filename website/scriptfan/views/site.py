#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Blueprint, render_template

sitemodular = Blueprint("site", __name__, url_prefix="/")

@sitemodular.route("/")
def index():
    return render_template("site/index.html")
