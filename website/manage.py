#!/usr/bin/env python
#-*-coding:utf-8-*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flaskext.script import Manager, Shell
from scriptfan import app, db, oid, config_app, dispatch_handlers, dispatch_apps

manager = Manager(app, with_default_commands=False)

def _make_context():
    return dict(app=app, db=db, oid=oid)

manager.add_command('shell', Shell(make_context=_make_context))

@manager.option('-c', '--config', dest='config', help='Configuration file name', default='scriptfan.cfg')
def runserver(config):
    config_app(app, config)
    dispatch_handlers(app)
    dispatch_apps(app)
    app.run(host='0.0.0.0')

@manager.option('-c', '--config', dest='config', help='Configuration file name', default='scriptfan.cfg')
def initdb(config='scriptfan.cfg'):
    config_app(app, config)
    from scriptfan.models import db

    try:
        db.drop_all()
        db.create_all()
        print 'Create tables success'
    except Exception as e:
        print 'Create tables fail:', e
        sys.exit(0)

if __name__ == '__main__':
    manager.run()
