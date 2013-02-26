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
from scriptfan.models import Event, EventDuration

from flask.ext.login import current_user


blueprint = Blueprint("events", __name__)


@blueprint.route('/', methods=['GET'])
def index():
    events = Event.query.all()
    return render_template('events/index.html', events=events)


@blueprint.route('/create', methods=['GET', 'POST'])
def create():
    form = EventForm(cref_enabled=False)
    if form.validate_on_submit():
        # TODO: Create event for more than one day.
        event = Event()
        duration = EventDuration()
        form.populate_obj(event)
        form.populate_obj(duration)
        event.durations.append(duration)

        # 装填用户和创建时间等信息
        event.user_id = current_user.user.id
        # TODO: 使用一些让SQLAlchemy能够自动更新模型中的 created_time 和 modified_time
        event.created_time = datetime.now()
        db.session.add(event)
        flash(u'活动%s发布成功.' % form.data.get('title'), 'success') 
        return redirect(url_for('events.index'))
    else:
        return render_template('events/create.html', form=form)
