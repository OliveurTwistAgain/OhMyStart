from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialisation de SQLAlchemy et Flask-Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='flaskstarter.config.DefaultConfig'):
    app = Flask(__name__)
    
    # Charger la configuration
    app.config.from_object(config_class)
    
    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Enregistrez les blueprints ici
    # Par exemple :
    # from .some_module import some_blueprint
    # app.register_blueprint(some_blueprint)

    # Autres configurations comme la gestion des erreurs, etc.
    
    return app
