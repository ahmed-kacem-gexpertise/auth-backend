from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import sys

# setting path
sys.path.append('..')
from config import Config




app = Flask(__name__)

app.config.from_object(Config)

bcrypt = Bcrypt( app )

db = SQLAlchemy(app)

migrate = Migrate(app, db)



from app import routes, models

