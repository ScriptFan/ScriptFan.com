#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Blueprint

news_modular = Blueprint("news", __name__, url_prefix="/news")
