from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    flash,
    current_app,
    request,
    make_response
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
)
from flask_principal import (
    identity_changed,
    Identity,
    session,
    AnonymousIdentity,
)

from werkzeug.exceptions import InternalServerError
from sqlalchemy.exc import IntegrityError
from random import randint
from datetime import datetime
from threading import Timer
from flask_socketio import emit

from web_app.models import (
    User,
    Role,
    db,
    socketio,
)
from web_app.login.login_forms import (
    LoginForm,
    RegForm,
    ConfirmForm
)
from . import login_app

from config import Config
from .SMS import sendSMS

login_data = {}


def clear_login_data():
    login_data['user'] = None
    login_data['code'] = None
    login_data['remb'] = None
    login_data['fresh'] = False
    login_data['remained'] = 0


def secunda():
    timer = Timer(1, secunda)
    remained = str(datetime.fromtimestamp(login_data['remained']).strftime('%M:%S'))
    socketio.emit('remained', {'data': remained}, namespace=login_data['namespace'])
    login_data['remained'] -= 1
    if login_data['remained'] < 0:
        timer.cancel()
        socketio.emit('time up', {'data': 'Время вышло, сэр!!!'})
        clear_login_data()
    else:
        timer.start()
    pass


@login_app.route('/', methods=['GET', 'POST'], endpoint='login')
def login():
    if current_user.is_authenticated:
        if current_user.role.role == 'admin':
            return redirect(url_for('admin_app.index'))
        return redirect(url_for('orders_app.orders'))
    if User.query.count() == 0:
        return redirect(url_for('login_app.register'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            #        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login_app.login'))

        login_data['user'] = user.id
        login_data['code'] = str(randint(100000, 999999))
        login_data['remb'] = form.remember_me.data
        login_data['fresh'] = True
        login_data['remained'] = 10
        if form.send_sms.data:
            sendSMS(login_data['code'])

        return redirect(url_for('login_app.confirm'))
    return render_template('login/login.html', title='Sign In', form=form)


@login_app.route('/confirm', methods=['GET', 'POST'], endpoint='confirm')
def confirm():
    form = ConfirmForm()
    if request.method == 'GET':
        if current_user.is_authenticated:
            if current_user.role.role == 'admin':
                return redirect(url_for('admin_app.index'))
            return redirect(url_for('orders_app.orders'))
        return render_template('login/confirm.html', form=form, code=login_data['code'])
    if form.validate_on_submit():
        if str(form.code.data) == login_data['code'] and login_data['fresh']:
            user = User.query.filter_by(id=login_data['user']).first()
            login_user(user, remember=login_data['remb'])
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
            if user.role.role == 'admin':
                return redirect(url_for('admin_app.index'))
            return redirect(url_for('orders_app.orders'))
    clear_login_data()
    return redirect(url_for('login_app.login'))



@login_app.route('/logout', endpoint='logout')
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('login_app.login'))


@login_app.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    form = RegForm()
    if request.method == 'GET':
        if User.query.count() > 0:
            return make_response('Нет такой страницы', 404)
        role = Role.query.filter_by(role='admin').one_or_none()
        if role is None:
            role = Role(id=1, role='admin')
            db.session.add(role)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                raise InternalServerError("failed to write admin role to the database")
        form.username.render_kw = {'value': 'admin'}
        choices = [(role.id, role.role)]
#        form.role.choices = [(role.id, role.role)]
        form.role.render_kw = {'value': choices[0][0]}
        form.phone.render_kw = {'value': '79272123456'}
        return render_template('login/register.html', form=form, choices=choices)
    if form.validate_on_submit():
        user = User(username='admin', id=1)
        user.set_password('1')
        user.role_id = int(form.role.data)
        user.phone_number = Config.PHONE
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise InternalServerError("failed to write admin user to the database")
        login_user(user, remember=True)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
        return redirect(url_for('admin_app.index'))
    return form.errors
    return {'user': form.username.data,
            'password': form.password.data,
            'password2': form.password2.data,
            'role': form.role.data,
            'phone': form.phone.data,
            'choices': form.role.choices}

# @socketio.on('my event')
# def test_message(message):
#     emit('my response', {'data': message['data']})
#
#
# @socketio.on('my broadcast event')
# def test_message(message):
#     emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})
    login_data['namespace'] = request.namespace
    secunda()


disconnect = 0


@socketio.on('disconnect')
def test_disconnect():
    global disconnect
    disconnect += 1
    print(f'Client disconnected {disconnect}')
