# flaskstarter/frontend/models.py

# -*- coding: utf-8 -*-

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user
from flask_admin.contrib import sqla
from ..extensions import db
from ..utils import get_current_time

# Declarer le modèle PlaceToVisit

class Lieu(db.Model):
    __tablename__ = 'placestovisit'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=get_current_time)
    nom = db.Column(db.String(255))
    description = db.Column(db.Text)
    ville = db.Column(db.String(255))
    pays = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    image_url = db.Column(db.String(255))
    url = db.Column(db.String(255))

    def __repr__(self):
        return f'<PlaceToVisit {self.id}>'

# Déclaration du modèle ContactUs
class ContactUs(db.Model):
    __tablename__ = 'contactus'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    sujet = db.Column(db.String(128), nullable=False)
    message = db.Column(db.String(2048), nullable=False)
    date_heure = db.Column(db.DateTime, default=get_current_time)

    def __repr__(self):
        _str = '%s. %s %s' % (self.id, self.name, self.email)
        return str(_str)

# Vue personnalisée pour ContactUs dans l'admin
class ContactUsAdmin(sqla.ModelView):
    column_sortable_list = ('id', 'nom', 'email', 'date_heure')
    column_filters = ('id', 'nom', 'email', 'date_heure')

    def __init__(self, session):
        super(ContactUsAdmin, self).__init__(ContactUs, session)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'
