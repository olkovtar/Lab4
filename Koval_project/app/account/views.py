from flask import Flask, render_template, request, session, redirect, url_for, flash, current_app
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlparse, urljoin

from .. import db, recaptcha
from .models import User
from .forms import RegistrationForm, LoginForm, UpdateAccountForm

from . import account_bp


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


@account_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = RegistrationForm()

    if form.validate_on_submit():
        if recaptcha.verify():
            user = User(username=form.username.data, email=form.email.data, password=form.password.data, normal_password=form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
                flash(f"Account created for {form.username.data}!", category='success')
            except:
                db.session.flush()
                db.session.rollback()
        else:
            flash(f"Do recaptcha", category='danger')

    return render_template('register.html', form=form)


@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home.home"))
        else:
            flash(f"Login unsuccessful. Email or password is incorrect!", category='danger')
    return render_template('login.html', form=form)


@account_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('home.home'))


@account_bp.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', all_users=all_users)


@account_bp.route('/users/delete/<id>')
def delete_user(id):
    db.session.delete(User.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for("account.users"))


@account_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    return render_template('account.html', form=form)
