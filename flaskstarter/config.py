# flaskstarter/config.py

# -*- coding: utf-8 -*-

import os

class BaseConfig(object):
    PROJECT = "flaskstarter"
    PROJECT_NAME = "flaskstarter.domain"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    BASE_URL = "https://yourdomain-flaskstarter.domain"
    ADMIN_EMAILS = ['admin@flaskstarter.domain']

    DEBUG = False
    TESTING = False

    SECRET_KEY = 'always-change-this-secret-key-with-random-alpha-nums'  # Remplacez par une clé secrète sécurisée

class DefaultConfig(BaseConfig):
    DEBUG = True

    # Flask-SQLAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BaseConfig.PROJECT_ROOT, "flaskstarter/db.sqlite")}'  # Chemin absolu pour la base de données

    # Flask-Cache
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # Flask-Mail
    MAIL_DEBUG = False
    MAIL_SERVER = "smtp.protonmail.com"  # Vérifiez si le serveur et le port sont corrects pour ProtonMail
    MAIL_PORT = 587  # Le port 1025 peut ne pas être correct pour ProtonMail, utilisez 587 ou 465 si nécessaire
    MAIL_USE_TLS = True
    MAIL_USERNAME = "oliveur.hoop@proton.me"
    MAIL_PASSWORD = "NzWhakatane64!"  # Assurez-vous que ce mot de passe est sécurisé et correct
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
