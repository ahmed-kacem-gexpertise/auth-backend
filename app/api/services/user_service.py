from ...models.user_model import User

from ...extensions import db
from flask_jwt_extended import get_jwt ,get_jwt_identity
def validate_user_path(user_id):
    try:
        logged_in_user_id = int(get_jwt_identity())  
        user_id = int(user_id) 
    except ValueError:
        return {"message": "Invalid user ID"}, 400  

    user = User.query.get(user_id)
    logged_in_user = User.query.get(logged_in_user_id)

    if not user:
        return {"message": "User not found"}, 404

    if not logged_in_user:
        return {"message": "Logged-in user not found"}, 404

    is_logged_in_user_admin = getattr(logged_in_user, 'admin', False)  

    if is_logged_in_user_admin or logged_in_user_id == user_id:
        return user 

    return {"message": "Unauthorized access"}, 403 


def add_user(data):
    if User.query.filter_by(email=data["email"]).first() :
        return False
    
         
    new_user = User(firstName=data["firstName"] ,lastName=data["lastName"] ,email=data["email"], admin=False)
    new_user.set_password(data["password"])
    new_user.save()
    return True
    


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

    
    