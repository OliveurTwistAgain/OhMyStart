# manage.py

# -*- coding: utf-8 -*-

import sys
import logging
from flask import Flask
from flask_migrate import Migrate
from flask.cli import with_appcontext
from flaskstarter import create_app, db
from flaskstarter.extensions import db, migrate
from flaskstarter.user.models import Users
from flaskstarter.user.constants import ADMIN, USER, ACTIVE, INACTIVE

# Configurer le logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Création de l'application
application = create_app()

# Initialisation de l'instance de Migrate
migrate = Migrate(application, db)

@application.cli.command("initdb")
@with_appcontext
def initdb():
    """Init/reset database."""
    print("Initialisation de la base de données...")
    db.drop_all()
    db.create_all()
    print("Tables de la base de données initialisées")

    # Création de l'utilisateur administrateur
    admin = Users(nom='Demo Admin',
                  email='oliveur.twist.again@proton.me',
                  password='adminpassword',
                  role_code=ADMIN,
                  status_code=ACTIVE)
    db.session.add(admin)

    # Création d'un utilisateur de démonstration
    user = Users(nom='Demo User',
                 email='oliveur.hoop@proton.me',
                 password='userpassword',
                 role_code=USER,
                 status_code=ACTIVE)
    db.session.add(user)

    db.session.commit()

    print("Database initialized with 2 users (admin, demo)")

if __name__ == "__main__":
    application.run()
