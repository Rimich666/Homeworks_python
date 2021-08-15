from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    flash
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
)

from web_app.models import User
from web_app.login.login_forms import LoginForm
from . import login_app


@login_app.route('/', methods=['GET', 'POST'], endpoint='login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('orders_app.orders'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
#        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login_app.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('orders_app.orders'))
    return render_template('login/login.html', title='Sign In', form=form)


@login_app.route('/logout', endpoint='logout')
def logout():
    logout_user()
    return redirect(url_for('login_app.login'))