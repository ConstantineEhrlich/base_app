# This is init file for the app class. Here we are importing everything that will be used:
# Flask
from flask import Flask
# the Config from the above folder
from config import Config
# the SQL ORD wrapper
from flask_sqlalchemy import SQLAlchemy
# the migration helper in order to upgrade database each time
# after each change in 'models', need to run 'flask db migrate -m "COMMENT"'.
# and then run 'flask db upgrade' - this will apply the migration script
from flask_migrate import Migrate
# login manager helper
from flask_login import LoginManager

app = Flask(__name__)
# standard flask method of  config.from_object(object)
# we are assigning the class Config imported from above
app.config.from_object(Config)
# db is the database, it takes the SQLALCHEMY_DATABASE_URI from the CONFIG
db = SQLAlchemy(app)
# migrate helper for the db
migrate = Migrate(app, db)
# login uses the LoginManager class from flask-login
login = LoginManager(app)
# to handle permissions, Flask-Login needs to know what is the view function that handles logins
# The 'login' value is the function (or endpoint) name for the login view.
login.login_view = 'login'


# then, we are importing the routes and models from the app
from app import routes, models

#this commit is test of Working Copy app
