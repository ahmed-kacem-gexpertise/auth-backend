# setup.py
import os
from .models.user_model import User
from .extensions import db

def create_database(app):
    """Creates databases and injects the main admin account into the user db."""
    
    with app.app_context():
        db.create_all()
        admin_exists = db.session.query(User).filter_by(admin=True).first()

        if not admin_exists:
            admin_email = os.getenv("ADMIN_EMAIL")
            admin_password = os.getenv("ADMIN_PASSWORD")
            admin_firstname = os.getenv("ADMIN_FIRSTNAME")
            admin_lastname = os.getenv("ADMIN_LASTNAME")

            if not all([admin_email, admin_password, admin_firstname, admin_lastname]):
                raise ValueError("One or more admin environment variables are missing!")

            # Create the admin user
            admin = User(
                firstName=admin_firstname,
                lastName=admin_lastname,
                email=admin_email,
                admin=True,
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()

