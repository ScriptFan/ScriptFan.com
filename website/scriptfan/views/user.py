#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import Blueprint, request, url_for, redirect, render_template, abort, flash, g
from flaskext.openid import COMMON_PROVIDERS
from daimaduan.variables import db, oid

usermodular = Blueprint("user", __name__, url_prefix="/user")

@userapp.route('/login/', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    form = LoginForm(request.form, csrf_enabled=False)
    if request.method == 'POST':
        openid = request.form.get('openid', None)
        if openid:
            return oid.try_login(COMMON_PROVIDERS.get(openid, "fackeone"),
                                 ask_for=['email', 'nickname'])
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                user.last_login_time = datetime.now()
                session['user'] = str(user.id)
                return redirect(request.args.get('next', '/'))
    g.form = form
    return render_template('userapp/login.html',
                           next=oid.get_next_url(),
                           error=oid.fetch_error())

@oid.after_login
def create_or_login(resp):
    session['openid'] = resp.identity_url
    user = User.query.filter_by(openid=resp.identity_url).first()
    if user is not None:
        flash(u'成功登入')
        session['user'] = str(user.id)
        session.pop('openid')
        g.user = getUserObject(user_id=session['user'])
        return redirect(oid.get_next_url())
    return redirect(url_for('userapp.create_profile',
                            next=oid.get_next_url(),
                            nickname=resp.nickname,
                            email=resp.email))

@userapp.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    form = ProfileForm(request.form)
    form.nickname.data = request.values.get('nickname')
    form.email.data = request.values.get('email')
    if request.method == 'POST' and form.validate():
        user = User(form.nickname.data,
                    form.email.data)
        user.openid = session['openid']
        info = UserInfo()
        user.info = info
        db.session.add(user)
        db.session.add(info)
        db.session.commit()
        flash(u'资料建立成功')
        session.pop('openid')
        return redirect(url_for('userapp.login'))
    g.form = form
    return render_template('userapp/create_profile.html', next_url=oid.get_next_url())

@userapp.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect('/')
