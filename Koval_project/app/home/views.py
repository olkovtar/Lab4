from flask import Flask, render_template, redirect, url_for
# import datetime as dt

from . import home_bp


@home_bp.route('/')
def about():
    # date = dt.datetime.now()
    return render_template('index.html', name='Welcome Page')



# Redirect
@home_bp.route('/home')
def home():
    return redirect(url_for('home.about'))
