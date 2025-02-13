from ...models.user_model import User
from flask import jsonify,make_response
from datetime import timedelta

from flask_jwt_extended import (
   create_access_token,
   create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
def authenticate(email, password,rememberMe):
    user = User.query.filter_by(email=email).first()
    if rememberMe:
        access_expires_in = timedelta(days=30)  
        refresh_expires_in = timedelta(days=30) 
    else:
        access_expires_in = timedelta(minutes=15) 
        refresh_expires_in = timedelta(days=7)  
    if user and user.verify_password(password):  
         
        access_token = create_access_token(identity=str(user.id),expires_delta=access_expires_in)
        refresh_token   = create_refresh_token(identity=str(user.id),expires_delta=refresh_expires_in)
        
      
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
    