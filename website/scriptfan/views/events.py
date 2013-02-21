# -*- coding: utf-8 -*-
"""
    scriptfan.views.events
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Views controllers for events
"""

from datetime import datetime

from flask import Blueprint, render_template, redirect, flash, url_for
from scriptfan import db
from scriptfan.forms import EventForm
from scriptfan.models import Event

from flask.ext.login import current_user


blueprint = Blueprint("events", __name__)


@blueprint.route('/', methods=['GET'])
def index():
    activities = Event.query.all()
    return render_template('events/index.html', activities=activities)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
    form = EventForm(cref_enabled=False)
    if form.validate_on_submit():
        activity = Event()
        form.populate_obj(activity)

        # 装填用户和创建时间等信息
        activity.user_id = current_user.user.id
        # TODO: 使用一些让SQLAlchemy能够自动更新模型中的 created_time 和 modified_time
        activity.created_time = datetime.now()
        db.session.add(activity)
        flash(u'活动%s发布成功.' % form.data.get('title'), 'success') 
        return redirect(url_for('.index'))
    else:
        return render_template('events/create.html', form=form)
