# flaskstarter/settings/forms.py

# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, EqualTo, Email
from flask_login import current_user
from ..user import Users
from ..utils import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX

class ProfileForm(FlaskForm):
    name = StringField('Name', [Length(max=50)])
    email = EmailField('Email', [InputRequired(), Email()])
    submit = SubmitField('Update')

    def validate_email(self, field):
        if Users.query.filter(Users.email.ilike(field.data), Users.id != current_user.id).first() is not None:
            raise ValidationError('This email is taken')

class PasswordForm(FlaskForm):
    password = PasswordField('Current password', [InputRequired()])
    new_password = PasswordField('New password', [InputRequired(), Length(min=PASSWORD_LEN_MIN, max=PASSWORD_LEN_MAX)])
    password_again = PasswordField('Password again', [InputRequired(), Length(min=PASSWORD_LEN_MIN, max=PASSWORD_LEN_MAX), EqualTo('new_password')])
    submit = SubmitField('Update')

    def validate_password(self, field):
        user = Users.query.filter_by(id=current_user.id).first()
        if not user or not user.check_password(field.data):
            raise ValidationError('Current password is incorrect')
