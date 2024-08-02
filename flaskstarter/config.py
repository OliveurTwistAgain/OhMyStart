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

    SECRET_KEY = 'always-change-this-secret-key-with-random-alpha-nums'

class DefaultConfig(BaseConfig):
    DEBUG = True

    # Flask-SQLAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BaseConfig.PROJECT_ROOT, "flaskstarter/db.sqlite")}'  # Corrected path

    # Flask-Cache
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # Flask-Mail
    MAIL_DEBUG = False
    MAIL_SERVER = ""
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "admin-mail@yourdomain-flaskstarter.domain"
    MAIL_PASSWORD = ""
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
