#!/usr/bin/env python
#-*-coding:utf-8-*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flaskext.script import Manager
from scriptfan import app, config_app, dispatch_handlers, dispatch_apps
from scriptfan.variables import *

manager = Manager(app)

@manager.option('-c', '--config', dest='config', help='Configuration file name')
def test(config):
    config_app(app, config)
    db.init_app(app)
    oid.init_app(app)
    dispatch_handlers(app)
    dispatch_apps(app)
    app.run(host='0.0.0.0')

@manager.option('-c', '--config', dest='config', help='Configuration file name')
def initialize(config):
    config_app(app, config)

    import pymongo
    host = app.config.get('MONGODB_HOST', 'localhost')
    port = app.config.get('MONGODB_PORT', 27017)
    conn = pymongo.Connection(host=host, port=port)
    if conn:
        try:
            conn.drop_database(app.config['MONGODB_DB'])
        except:
            pass

    db.init_app(app)

    print "Start to add all syntax"
    from daimaduan.models.syntax import ALL_SYNTAX
    from daimaduan.models import User, Syntax, Tag, Paste
    for lexer in ALL_SYNTAX:
        syntax = Syntax(name=lexer[0], tag=lexer[1].lower())
        try:
            syntax.save()
        except:
            pass

    print u'Start to add 未注册用户'
    import random
    user = User(nickname=u'未注册用户', email='user@daimaduan.com',
                password=''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 8)))
    try:
        user.save()
    except Exception, e:
        pass

@manager.option('-c', '--config', dest='config', help='Configuration file name')
def generate_test(config):
    config_app(app, config)
    db.init_app(app)

    from daimaduan.models import User, Syntax, Tag, Paste
    user1 = User(nickname='davidx',
                email='david.xie@me.com',
                password=hashPassword('123456'))
    user1.save()
    user2 = User(nickname='zhangkai',
                email='zhangkai@daimaduan.com',
                password=hashPassword('123456'))
    user2.save()
    user3 = User(nickname='guest',
                email='guest@daimaduan.com',
                password=hashPassword('123456'))
    user3.save()

    users = [user1, user2, user3]

    from tests import FILES
    import random
    for filename, syntax, tags in FILES:
        syntax = Syntax.objects(name=syntax).first()
        f = open('tests/%s' % filename, 'r')
        paste = Paste(title=filename,
                      user=users[random.randint(0, 2)],
                      syntax=syntax,
                      content=f.read())
        paste.save()
        for tag in tags:
            t = Tag.objects(name=tag).first()
            if not t:
                t = Tag(name=tag)
                t.save()
            paste.tags.append(t)
        paste.save()
        f.close()

if __name__ == '__main__':
    manager.run()

