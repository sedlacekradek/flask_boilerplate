from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo
import email_validator
from wtforms import ValidationError
from .models import User
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    EmailField,
    SelectField,
    TextAreaField,
    DateField,
    BooleanField
)



### AUTH FORMS ###
class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(5, 64), Email()])
    name = StringField('Name', validators=[DataRequired(), Length(2, 64)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(fieldname='password_repeat',
                                                                             message='Passwords must match.')])
    password_repeat = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    # custom validator - raise error if mail already used
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email is already registered.')

    # custom validator - raise error if username already used
    def validate_name(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This name is already registered.')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(5, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class ResetForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(5, 64), Email()])
    submit = SubmitField('Request Reset')


class NewPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(fieldname='password_repeat',
                                                                             message='Passwords must match.')])
    password_repeat = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Set new password')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo(fieldname='password_repeat',
                                                                             message='Passwords must match.')])
    password_repeat = PasswordField('Repeat New Password', validators=[DataRequired()])
    submit = SubmitField('Set new password')