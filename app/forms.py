# some special form classes from flask:
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


# class LoginForm of FlaskForm, that is provided with some variables:
class LoginForm(FlaskForm):
    # each form field is provided with it's label and some validators:
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('User Name:', validators=[DataRequired()])
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    password_check = PasswordField('Repeat password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # validate_<field_name> -- WTForms takes those as custom validators
    # and invokes them in addition to the stock validators
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Choose another username!!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Choose another email')


class RecordForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired()])
    comment = StringField('Comment')
    submit = SubmitField('Submit')

    def validate_amount(self, amount):
        if self.amount == 0:
            raise ValidationError('Amount cannot be zero')
