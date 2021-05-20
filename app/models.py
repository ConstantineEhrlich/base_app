# This is models file
# It is responsible for business objects
# Here we create classes for different entities,
# and link it to the database structure

# in order to update database in accordance with the models
# after each change in 'models', need to run 'flask db migrate -m "COMMENT"'.
# and then run 'flask db upgrade' - this will apply the migration script


# import the db from app (we've assigned sqlalchemy to it)
from app import db
from datetime import datetime
# useful tools for security:
from werkzeug.security import generate_password_hash, check_password_hash
# mixin is an "additional" subclass that adds some functionality to User class
from flask_login import UserMixin
# import flask-login functionality
from app import login


# User class
# mix-in is to add attributes from other class to this one
class User(UserMixin, db.Model):
    # custom table name (because i love when table is plural)
    __tablename__ = 'users'

    # User class variables, that are also initialized as DB columns
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(256))

    # relationship with other entities as VARIABLE
    # db.relationship('CLASS', backref='VARIABLE', lazy='dynamic')
    records = db.relationship('Record', backref='author', lazy='dynamic')

    # print itself:
    def __repr__(self):
        return 'User: ' + format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# flask-login expects that the application will configure a user loader function
# that can be called to load a user given the ID
# this provides entities like current_user
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Record class
class Record(db.Model):
    # custom table name:
    __tablename__ = 'records'

    # table columns / class attributes:
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False, default=0)
    comment = db.Column(db.String(120), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    record_type = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # print itself
    def __repr__(self):
        return 'Record: ' + str(self.amount) + ' by ' + str(self.user_id)
