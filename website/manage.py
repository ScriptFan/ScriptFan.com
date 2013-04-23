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

@manager.option('-l', '--lang', dest='lang', help='Language to translate', default=None)
def translate(lang):
    if lang:
        dirs = [lang,]
    else:
        trans_dir = os.path.join('scriptfan', 'translations')
        dirs = os.listdir(trans_dir)
    try:
        import subprocess
        print 'Scanning translations under path:', trans_dir
        for language in dirs:
            message_dir  = os.path.join(trans_dir, language, 'LC_MESSAGES')
            message_source = os.path.join(message_dir, 'messages.pot')
            message_target = os.path.join(message_dir, 'messages.mo')
            if os.path.exists(message_source):
                print '  Translateing', language, 'messages...'
                args = ['msgfmt', message_source, '-o', message_target, '-v']
                cmd = " ".join(args)
                pin, pout = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE).communicate()
                for line in pout.split('\n'):
                    print ' ', line
    except Exception as e:
        print '  Translateing failed:', e

if __name__ == '__main__':
    manager.run()
