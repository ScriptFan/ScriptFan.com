#!/usr/bin/env python
#-*-coding:utf-8-*-
import logging
logger = logging.getLogger(__name__)

from flask import Blueprint, render_template
from scriptfan.forms.activity import ActivityForm

activityapp = Blueprint("activity", __name__)

@activityapp.route('/', methods=['GET'])
def index():
    return render_template('activities/index.html')

@activityapp.route('/create', methods=['GET'])
def create():
    form = ActivityForm(cref_enabled=False)
    return render_template('activities/create.html', form=form)
