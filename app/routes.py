# this is routes file. it is responsible for the webpage rendering
# render_template returns the webpage
# flash is "hidden message" passed from page to page
# redirect is obvious
# url_for returns the url for specific function by referring to function name - urf_for('index')
import datetime

from flask import render_template, flash, redirect, url_for, request
from app import app
# also import the forms!
from app.forms import *
# import user sessions functionality
from flask_login import current_user, login_user, logout_user, login_required
# in order to link the models, import it too
from app.models import *
from werkzeug.urls import url_parse


# index page is returned both on / and /index
@app.route('/')
@app.route('/index')
def index():
    # define some variables
    records = Record.query.order_by(Record.timestamp.desc()).all()
    # render template index.html and pass some variables to it
    return render_template('index.html', title='Home', records=records)


# for login page, the POST method will be used
@app.route('/login', methods=['GET', 'POST'])
def login():
    # check if there is active session:
    # The current_user variable comes from Flask-Login and can be used at any
    # time during the handling to obtain the user object that represents the client of the request.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # LoginForm is a class from forms.py
    form = LoginForm()

    # the following code is called when form is submitted:
    if form.validate_on_submit():
        # returns SELECT FIRST FROM USERS WHERE users.username = ...
        user = User.query.filter_by(username=form.username.data).first()
        # check if invalid user or password
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username of password')
            return redirect(url_for('login'))
        # if didnt handle on previous step, proceed with login
        flash('Successful login for {} at {}'.format(user.username, datetime.now().strftime('%H:%M:%S')))
        login_user(user, remember=form.remember_me.data)

        # The following handles the case when the decorator
        # @login_required is applied to the route:
        # the link which requires login will be passed as 'next' in the
        # GET request, for example if 'profiles' is restricted: /login?next=/profiles.
        next_page = request.args.get('next')
        # An attacker could insert a URL to a malicious site in the next argument,
        # so the application only redirects when the URL is relative, which ensures
        # that the redirect stays within the same site as the application. To determine
        # if the URL is relative or absolute, it is passed to url_parse()
        # function and then check if the netloc component is set or not.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    # normally - render login template
    return render_template('login.html', title='Sign In', form=form)


# logs user out
@app.route('/logout')
def logout():
    flash('User {} logged out @ {}'.format(current_user.username, datetime.now().strftime('%H:%M:%S')))
    logout_user()
    return redirect(url_for('index'))


# registration form
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('New user registered: {} @ {}'.format(user.username, datetime.now().strftime('%H:%M:%S')))
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Profiles page
@app.route('/profiles')
@login_required
def profiles():
    users = User.query.all()
    return render_template('profiles.html', users=users, title='Profiles')


# Profile page
@app.route('/profiles/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    records = Record.query.filter_by(author=user).order_by(Record.timestamp.desc())
    count = records.count()
    title = 'Profile of ' + user.username
    return render_template('index.html', user=user, records=records, title=title, count=count)


# Create Record page
@app.route('/newrecord', methods=['POST', 'GET'])
@login_required
def newrecord():
    form = RecordForm()
    if form.validate_on_submit():
        record = Record(amount=form.amount.data, author=current_user, comment=form.comment.data)
        db.session.add(record)
        db.session.commit()
        flash('New record created successfully!')
        return redirect(url_for('index'))
    return render_template('newrecord.html', title='New record', form=form)
