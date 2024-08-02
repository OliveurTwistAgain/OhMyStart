# -*- coding: utf-8 -*-

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user
from flask_admin.contrib import sqla
from ..extensions import db
from ..utils import get_current_time

# Déclaration du modèle Monument
class Monument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    id_users = db.Column(db.Integer, db.ForeignKey('users.id'))  # Associé à la table des utilisateurs

    # Relation avec le modèle Users
    user = db.relationship('Users', backref=db.backref('monuments', lazy=True))

    def __repr__(self):
        return f'<Monument {self.name}>'

# Déclaration du modèle Users
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # Ajoutez d'autres champs nécessaires pour les utilisateurs

# Déclaration du modèle ContactUs
class ContactUs(db.Model):
    __tablename__ = 'contactus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    subject = db.Column(db.String(128), nullable=False)
    message = db.Column(db.String(2048), nullable=False)
    received_time = db.Column(db.DateTime, default=get_current_time)

    def __unicode__(self):
        _str = '%s. %s %s' % (self.id, self.name, self.email)
        return str(_str)

# Vue personnalisée pour ContactUs dans l'admin
class ContactUsAdmin(sqla.ModelView):
    column_sortable_list = ('id', 'name', 'email', 'received_time')
    column_filters = ('id', 'name', 'email', 'received_time')

    def __init__(self, session):
        super(ContactUsAdmin, self).__init__(ContactUs, session)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'
