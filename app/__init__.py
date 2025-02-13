from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .extensions import db , jwt , migrate , bcrypt,endpoints,email_service
from .db_utils import create_database
from .api.resources.auth_api import auth_ns
from .api.resources.user_api import user_ns
from .api.services.email_service import EmailService
from .config import Config

app = Flask(__name__)
def create_app():

    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    email_service.init_app(app)
    endpoints.init_app(app)
    endpoints.add_namespace(auth_ns)
    endpoints.add_namespace(user_ns)
    
    create_database(app)
    return app
