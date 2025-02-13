# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restx import Api
from .api.services.email_service import EmailService
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
bcrypt= Bcrypt()
endpoints = Api()
email_service = EmailService()
endpoints.authorizations = {
    "Cookie Auth": {
        "type": "apiKey",
        "in": "cookie",
        "name": "token",  
        "description": "JWT token stored in an httpOnly cookie is sent automatically with each request"
    }
}

