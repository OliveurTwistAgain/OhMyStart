# flaskstarter/extensions.py

# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_caching import Cache
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_migrate import Migrate

# Instances des extensions
db = SQLAlchemy()
mail = Mail()
cache = Cache()
login_manager = LoginManager()
login_manager.login_view = "frontend.login"  # Assurez-vous que cette vue existe
login_manager.login_message = "Please login or signup to add a new trip"

class HomeView(AdminIndexView):
    def is_visible(self):
        return False

# Instance de flask-admin
admin = Admin(name='Flask-Starter Admin', template_mode='bootstrap3', index_view=HomeView(name='Home'))
admin.add_link(MenuLink(name='Back to Dashboard', url='/dashboard', icon_type='glyph', icon_value='glyphicon-circle-arrow-left'))
admin.add_link(MenuLink(name='Logout', url='/logout', icon_type='glyph', icon_value='glyphicon-log-out'))

# Instance de Migrate
migrate = Migrate()
