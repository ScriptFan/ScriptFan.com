#!/usr/bin/env python
#-*-coding:utf-8-*-
import time
from flask import Flask
from app import config_app, dispatch_apps, dispatch_handlers

app = Flask(__name__)
