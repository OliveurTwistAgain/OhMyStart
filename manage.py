# -*- coding: utf-8 -*-

from flask import current_app
from flask_migrate import Migrate
from flaskstarter import create_app
from flaskstarter.extensions import db
from flaskstarter.user import Users, ADMIN, USER, ACTIVE

# Création de l'application
application = create_app()
migrate = Migrate(application, db)

@application.cli.command("initdb")
def initdb():
    """Init/reset database."""
    db.drop_all()  # Supprime toutes les tables de la base de données
    db.create_all()  # Crée toutes les tables

    # Création de l'utilisateur administrateur
    admin = Users(name='Admin Flask-Starter',
                  email=u'admin@your-mail.com',
                  password=u'adminpassword',
                  role_code=ADMIN,
                  status_code=ACTIVE)

    db.session.add(admin)

    # Création d'un utilisateur de démonstration
    for i in range(1, 2):
        user = Users(name='Demo User',
                     email=u'demo@your-mail.com',
                     password=u'demopassword',
                     role_code=USER,
                     status_code=ACTIVE)
        db.session.add(user)

    db.session.commit()  # Enregistrement des modifications dans la base de données

    print("Database initialized with 2 users (admin, demo)")

if __name__ == "__main__":
    application.run()
