#!/usr/bin/env python
#-*-coding:utf-8-*-
import logging
logger = logging.getLogger(__name__)

from flask import Blueprint, render_template, redirect, flash, url_for
from scriptfan.extensions import db
from scriptfan.forms.activity import ActivityForm
from scriptfan.models import Activity

from flask.ext.login import current_user

activityapp = Blueprint("activity", __name__)

@activityapp.route('/', methods=['GET'])
def index():
    return render_template('activities/index.html')

@activityapp.route('/create', methods=['GET', 'POST'])
def create():
    form = ActivityForm(cref_enabled=False)
    if form.validate_on_submit():
        activity = Activity()
        form.populate_obj(activity)

        # 装填用户和创建时间等信息
        activity.user_id = current_user.user.id
        db.session.add(activity)
        flash(u'活动%s发布成功.' % form.data.get('title'), 'success') 
        return redirect(url_for('.index'))
    else:
        return render_template('activities/create.html', form=form)
