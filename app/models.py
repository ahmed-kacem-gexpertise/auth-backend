from app import db 

import enum


class UserRoleEnum(enum.Enum):
    admin = 'admin'
    collector = 'user'

class User(db.Model):
    __tablename__ = "users"
    id = db.Column( db.Integer, primary_key=True ,autoincrement=True ) #assigns an id as a primary Key
    email = db.Column( db.String, unique = True ) #each email given has to be unique
    password = db.Column(db.String(128)) 
    
    











