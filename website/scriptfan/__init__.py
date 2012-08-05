#!/usr/bin/env python
#-*-coding:utf-8-*-
import os
from flask import Flask, render_template, abort
from extensions import oid, db, login_manager

instance_path = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, instance_path=instance_path, instance_relative_config=True)

def config_app(app, config):
    app.debug_log_format = '[%(levelname)s] %(message)s'
    app.config.from_pyfile(config)
    config_logger(app)
    db.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    
    @app.after_request
    def after_request(response):
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(500)
        return response

def config_logger(app):
    # import logging, logging.config
    # if not os.path.exists(app.config['LOGGER_DIR']):
    #     os.makedirs(app.config['LOGGER_DIR'])
    # logging.config.dictConfig(app.config['LOGGER_CONFIG'])
    # app.logger.error(app.logger.name)
    pass

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

def dispatch_apps(app):
    from scriptfan.views import siteapp, userapp
    app.register_blueprint(siteapp,  url_prefix='/')
    app.register_blueprint(userapp,  url_prefix='/user')

    from scriptfan.utils.filters import dateformat, empty, time_passed
    app.jinja_env.filters['dateformat'] = dateformat
    app.jinja_env.filters['empty'] = empty
    app.jinja_env.filters['time_passed'] = time_passed
