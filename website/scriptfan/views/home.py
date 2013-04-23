# -*- coding: utf-8 -*-
"""
    scriptfan.views.home
    ~~~~~~~~~~~~~~~~~~~~~~~
    Home view controller
"""

from flask import Blueprint, render_template, make_response


blueprint = Blueprint('home', __name__)


@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/enviroment.js')
def env():
    # TODO: Enable cache for global enviroment scripts
    response = make_response(render_template('enviroment.js'))
    response.headers['Content-Type'] = 'text/javascript; charset=utf-8'
    return response
