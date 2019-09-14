from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from project.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rmbr_user = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegisterNewUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    password_confirm = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    multi_fac_auth = BooleanField('I want Multifactor Authentication')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter(User.username == username.data).first()
        if user is not None:
            raise ValidationError('Username has already been taken')

    def validate_email(self, email):
        user = User.query.filter(User.email == email.data).first()
        if user is not None:
            raise ValidationError('Email has already been taken')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class PasswordResetForm(FlaskForm):
    password = StringField('Password', validators=[DataRequired()])
    password_confirm = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
