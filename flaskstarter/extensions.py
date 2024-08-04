# flaskstarter/extensions.py

# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_caching import Cache
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_migrate import Migrate
from flask_login import LoginManager

# Instances des extensions
login_manager = LoginManager()

# Configuration de LoginManager
login_manager.login_view = "frontend.login"
login_manager.login_message = "Svp, connectez-vous pour accéder à cette page."

# Instances des autres extensions
db = SQLAlchemy()
mail = Mail()
cache = Cache()

class HomeView(AdminIndexView):
    def is_visible(self):
        return False

# Instance de flask-admin
admin = Admin(name='Flask-Starter Admin', template_mode='bootstrap3', index_view=HomeView(name='Home'))
admin.add_link(MenuLink(name='Back to Dashboard', url='/dashboard', icon_type='glyph', icon_value='glyphicon-circle-arrow-left'))
admin.add_link(MenuLink(name='Logout', url='/logout', icon_type='glyph', icon_value='glyphicon-log-out'))

# Instance de Migrate
migrate = Migrate()
