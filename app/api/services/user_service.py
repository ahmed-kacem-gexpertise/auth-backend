from ...models.user_model import User
from ...models.black_listed_tokens import BlacklistedToken

from ...extensions import db
from flask_jwt_extended import get_jwt ,get_jwt_identity
def validate_user_path(user_id):
    logged_in_user_id = int(get_jwt_identity() ) 
    is_logged_in_user_admin=get_jwt()['admin']
    user = User.query.get(user_id)  
    
    if not user :
        return None 
    if is_logged_in_user_admin or logged_in_user_id == user_id:
        return user
    return False

def add_user(data):
    if User.query.filter_by(email=data["email"]).first() :
        return False
    
         
    new_user = User(firstName=data["firstName"] ,lastName=data["lastName"] ,email=data["email"], admin=False)
    new_user.set_password(data["password"])
    new_user.save()
    return True
    

def delete_user(user_id):
    user_to_delete=validate_user_path(user_id)
    if  user_to_delete:
        jti = get_jwt()["jti"]

        # Blacklist the current token
        blacklisted_token = BlacklistedToken(jti=jti)
        db.session.add(blacklisted_token)
        
        # Delete user from database
        db.session.delete(user_to_delete)
        db.session.commit()
        return True
    return False
def get_user_info(user_id):
    user = validate_user_path(user_id)
    return user
def update_user(data,user_id):
    user:User = validate_user_path(user_id)
    if not user :
        return False
    
    user.update_info(**data)
    return True


def change_user_password(data):
    old_password=data['old_password']
    new_password=data['new_password']
    user_identity=get_jwt_identity()
    user= User.query.get(user_identity)
    if old_password != new_password and user.verify_password(old_password):
        user.set_password(new_password)
        return True
    return False        
    
    