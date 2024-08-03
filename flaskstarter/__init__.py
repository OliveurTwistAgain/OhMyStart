# flaskstarter/__init__.py

# Initialisation de l'application Flask

from flask import Flask
from flask_migrate import Migrate
from .extensions import db, mail, cache, login_manager, admin

# Initialisation de Flask-Migrate
migrate = Migrate()

def create_app(config_class='flaskstarter.config.DefaultConfig'):
    app = Flask(__name__)
    
    # Charger la configuration
    app.config.from_object(config_class)
    
    # Initialisation des extensions
    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db)

    # Enregistrement des blueprints
    from .frontend.views import frontend
    from .settings.views import settings
    
    app.register_blueprint(frontend)
    app.register_blueprint(settings)

    return app
