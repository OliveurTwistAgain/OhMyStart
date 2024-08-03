# flaskstarter\app.py

# -*- coding: utf-8 -*-

from flask import Flask
from .config import DefaultConfig
from .user import Users, UsersAdmin
from .settings import settings
from .frontend import frontend, ContactUsAdmin
from .extensions import db, mail, cache, login_manager, admin
from .utils import INSTANCE_FOLDER_PATH, pretty_date

# For import *
__all__ = ['create_app']

DEFAULT_BLUEPRINTS = (
    frontend,
    settings,
)

def create_app(config=None, app_name=None, blueprints=None):
    if app_name is None:
        app_name = DefaultConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name,
                instance_path=INSTANCE_FOLDER_PATH,
                instance_relative_config=True)

    configure_app(app, config)
    configure_extensions(app)
    configure_blueprints(app, blueprints)
    configure_logging(app)
    configure_template_filters(app)
    configure_error_handlers(app)

    return app

def configure_app(app, config=None):
    app.config.from_object(DefaultConfig)
    app.config.from_pyfile('production.cfg', silent=True)
    if config:
        app.config.from_object(config)

def configure_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    admin.add_view(ContactUsAdmin(db.session))
    admin.add_view(UsersAdmin(db.session))
    admin.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Update this to match your login view

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

def configure_template_filters(app):
    @app.template_filter()
    def _pretty_date(value):
        return pretty_date(value)

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)

def configure_logging(app):
    if app.debug:
        return

def configure_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_page(error):
        return "Oops! You don't have permission to access this page.", 403

    @app.errorhandler(404)
    def page_not_found(error):
        return "Oops! Page not found.", 404

    @app.errorhandler(500)
    def server_error_page(error):
        return "Oops! Internal server error. Please try after sometime.", 500
