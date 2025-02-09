# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restx import Api
db = SQLAlchemy()
from .models.black_listed_tokens import BlacklistedToken
jwt = JWTManager()
migrate = Migrate()
bcrypt= Bcrypt()
endpoints = Api()
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_data):
    jti = jwt_data["jti"]
    # Check if the token exists in the blacklist
    return db.session.query(BlacklistedToken).filter_by(jti=jti).first() is not None
endpoints.authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Enter token as 'Bearer <your-token>'"
    }
}
