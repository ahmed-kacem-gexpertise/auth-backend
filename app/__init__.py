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
