#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Blueprint, render_template

siteapp = Blueprint("site", __name__)

@siteapp.route("/")
def index():
    return render_template("index.html")
