# -*-coding: utf-8-*-
"""
    scriptfan.models.event_duration
    ~~~~~~~~~~~~~~~~~~~~~~

    Model for table: event_durations
"""

from scriptfan import db

class EventDuration(db.Model):
    """Event duration assignment

    Samples:
     * 1 Day
        - Date: 2013-03-16, Start_Time: 13:30, End_Time: 17:00
     * 2 Days
        - Date: 2013-03-16, Start_Time: 09:00, End_Time: 17:00
        - Date: 2013-03-17, Start_Time: 09:30, End_Time: 11:30

    It seems that ScriptFan will not create an event that repeats by
    week/month/year, so the data model is enough.
    """

    __tablename__ = 'event_durations'

    id = db.Column(db.Integer, primary_key=True)

    #: Date part o event. 2013-03-16
    date = db.Column(db.Date)
    #: Start time of date part. 13:30
    start_time = db.Column(db.Time, default='13:30')
    #: End time of date part.   17:00
    end_time   = db.Column(db.Time, default='17:00')

    #: Related event of time duration
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)