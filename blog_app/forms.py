from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator
from blog_app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first() # if not exists returns None

        if user:
            raise ValidationError('This username is already taken!')

    def validate_email(self, email):

        mail = User.query.filter_by(email=email.data).first() # if not exists returns None

        if mail:
            raise ValidationError('This E-Mail is already taken!')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first() # if not exists returns None

            if user:
                raise ValidationError('This username is already taken!')

    def validate_email(self, email):
        if email.data != current_user.email:
            mail = User.query.filter_by(email=email.data).first() # if not exists returns None

            if mail:
                raise ValidationError('This E-Mail is already taken!')