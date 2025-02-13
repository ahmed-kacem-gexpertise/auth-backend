from ...models.user_model import User
from flask import jsonify,make_response
from flask_jwt_extended import (
   create_access_token,
   create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    
    if user and user.verify_password(password):  
         
        access_token = create_access_token(identity=str(user.id))
        refresh_token   = create_refresh_token(identity=str(user.id))
        
      
        response_data = {
            'message': 'Login successful',
        }
        
        resp = jsonify(response_data)

         
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)

        
        return resp
    
    
    return None
def confirm_user_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        user.confirm_user()
        return user
    return None
def check_user_exists(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return user
    return None
    