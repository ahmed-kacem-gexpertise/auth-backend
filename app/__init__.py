from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import sys
from flask_jwt_extended import JWTManager
import os
load_dotenv()

# setting path
sys.path.append('..')
from config import Config




app = Flask(__name__)

app.config.from_object(Config)

bcrypt = Bcrypt( app )

db = SQLAlchemy(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)


from app import routes, models

from app.models import User

def create_databases():
    """Creates databases and injects the main admin account into the user db"""

    with app.app_context():  # Ensure we are within the application context
        db.create_all()  # Creates tables if they do not exist

        # Check if an admin already exists
        if not db.session.execute(db.select(User).filter_by(role=True)).scalar_one_or_none():
            admin_email = os.getenv("ADMIN_EMAIL")
            admin_password = os.getenv("ADMIN_PASSWORD")

            if not admin_email or not admin_password:
                raise ValueError("Admin email or password is not set in environment variables.")

            # Hash the password before storing it
            hashed_password = bcrypt.generate_password_hash(admin_password).decode("utf-8")

            admin = User(
                email=admin_email,
                password=hashed_password,
                role=True,
            )
            db.session.add(admin)
            db.session.commit()
        
        db.session.close() 
create_databases()