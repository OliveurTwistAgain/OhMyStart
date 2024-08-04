# flaskstarter/frontend/forms.py

# -*- coding: utf-8 -*-

import sys
from markupsafe import Markup
from flask_wtf import FlaskForm
from wtforms import (ValidationError, HiddenField, BooleanField, StringField,
                     PasswordField, SubmitField, TextAreaField, EmailField, URLField, DecimalField)
from wtforms.validators import InputRequired, Length, EqualTo, Email, DataRequired, Optional, URL

from ..utils import (NAME_LEN_MIN, NAME_LEN_MAX, PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)
from ..user import Users

terms_html = Markup('<a target="blank" href="/terms">Terms of Service</a>')

class LoginForm(FlaskForm):
    next = HiddenField()
    login = EmailField(u'Email', [InputRequired()])
    password = PasswordField('Password', [InputRequired(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class SignupForm(FlaskForm):
    next = HiddenField()
    name = StringField(u'Name', [InputRequired(), Length(NAME_LEN_MIN, NAME_LEN_MAX)])
    email = EmailField(u'Email', [InputRequired(), Email()])
    password = PasswordField(u'Password', [InputRequired(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)], description=u'6 or more characters.')
    agree = BooleanField(u'Agree to the ' + terms_html, [InputRequired()])
    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if Users.query.filter(Users.email.ilike(field.data)).first() is not None:
            raise ValidationError(u'Cet email est déjà enregistré')

class RecoverPasswordForm(FlaskForm):
    email = EmailField(u'Your email', [Email()])
    submit = SubmitField('Send instructions')

class ChangePasswordForm(FlaskForm):
    email_activation_key = HiddenField()
    email = HiddenField()
    password = PasswordField(u'Password', [InputRequired(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    password_again = PasswordField(u'Password again', [EqualTo('password', message="Le mot de passe ne correspond pas")])
    submit = SubmitField('Save')

class ContactUsForm(FlaskForm):
    nom = StringField(u'Nom', [InputRequired(), Length(max=64)])
    email = EmailField(u'Email', [InputRequired(), Email(), Length(max=64)])
    sujet = StringField(u'Sujet', [InputRequired(), Length(5, 128)])
    message = TextAreaField(u'Message', [InputRequired(), Length(10, 1024)])
    submit = SubmitField('Envoyer')

class LieuForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    ville = StringField('Ville', validators=[Optional()])
    pays = StringField('Pays', validators=[Optional()])
    image_url = URLField('URL de l\'image', validators=[Optional()])
    latitude = DecimalField('Latitude', validators=[Optional()], places=6)
    longitude = DecimalField('Longitude', validators=[Optional()], places=6)
    submit = SubmitField('Enregistrer')

