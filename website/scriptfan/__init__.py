# -*- coding: utf-8 -*-
"""
    scriptfan
    ~~~~~~~~~~~~~~

    Module to initialize and config flask application.
"""

import os
from flask import Flask, render_template, abort, url_for
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.babel import Babel

# Create extension instances
oid = OpenID()
db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()


# Create flask application instance
instance_path = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, instance_path=instance_path, \
                      instance_relative_config=True)
app.debug_log_format = '[%(levelname)s] %(message)s'
app.debug = True

# Configuration application
def config_app(app, config):
    app.logger.info('Setting up application...')
   
    app.logger.info('- Loading config file: %s' % config)
    app.config.from_pyfile(config)

    app.logger.info('- Setting up extensions...')
    db.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)

    @app.after_request
    def after_request(response):
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(500)
        return response


def dispatch_handlers(app):
    d = {}
    @app.errorhandler(403)
    def permission_error(error):
        d['title'] = u'您没有权限'
        d['message'] = u'您没有权限执行当前的操作, 请登陆或检查url是否错误.'
        return render_template('error.html', **d), 403

    @app.errorhandler(404)
    def page_not_found(error):
        d['title'] = u'页面不存在'
        d['message'] = u'您所访问的页面不存在, 是不是打错地址了啊?'
        return render_template('error.html', **d), 404

    @app.errorhandler(500)
    def page_error(error):
        d['title'] = u'页面出错啦'
        d['message'] = u'您所访问的页面出错啦! 待会再来吧!'
        return render_template('error.html', **d), 500


def register_blueprints(app):
    app.logger.info('Register blueprints...')
    from scriptfan.views import home, events, users
    app.register_blueprint(home.blueprint,   url_prefix='/')
    app.register_blueprint(users.blurprint,  url_prefix='/users')
    app.register_blueprint(events.blueprint, url_prefix='/events')


def register_jinja_env(app):
    app.logger.info('Register jinja filters...')
    from scriptfan import filters
   
    for filter in filters.__all__:
        app.logger.info('- Register filter: %s' % filter)
        app.jinja_env.filters[filter] = getattr(filters, filter)
    
    app.logger.info('Register jinja variables...')
    app.jinja_env.globals['static'] = (lambda filename: \
            url_for('static', filename=filename))
