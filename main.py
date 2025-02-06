from app import app

from app.models import User

from app import db

from flask_session import Session 
from flask_bcrypt import Bcrypt

from flask_cors import CORS

CORS(app, supports_credentials=True)


if __name__ == '__main__':
    app.run(port=5555, debug=True)