#!/usr/bin/env python
#-*-coding:utf-8-*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask.ext.script import Manager, Shell
from scriptfan import app, db, oid, config_app, dispatch_handlers, \
                      register_blueprints, register_jinja_env

manager = Manager(app, with_default_commands=False)

def _make_context():
    return dict(app=app, db=db, oid=oid)

manager.add_command('shell', Shell(make_context=_make_context))

@manager.option('-c', '--config', dest='config', help='Configuration file name', default='scriptfan.cfg')
@manager.option('-H', '--host',   dest='host',   help='Host address', default='0.0.0.0')
@manager.option('-p', '--port',   dest='port',   help='Application port', default=5000)
def runserver(config, host, port):
    config_app(app, config)
    dispatch_handlers(app)
    register_blueprints(app)
    register_jinja_env(app)
    app.run(host=host, port=port)

@manager.option('-c', '--config', dest='config', help='Configuration file name', default='scriptfan.cfg')
def initdb(config='scriptfan.cfg'):
    config_app(app, config)

    try:
        db.drop_all()
        db.create_all()
        print 'Create tables success'
    except Exception as e:
        print 'Create tables fail:', e
        sys.exit(0)

if __name__ == '__main__':
    manager.run()
