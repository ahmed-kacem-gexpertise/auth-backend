from ...models.user_model import User
from flask_jwt_extended import create_access_token
def authenticate(email,password):
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        additional_claims = {"admin": user.admin}
        access_token = create_access_token(identity=f"{user.id}",additional_claims=additional_claims)
        return access_token
    return None
