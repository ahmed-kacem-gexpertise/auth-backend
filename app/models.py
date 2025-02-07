from app import db , bcrypt

import enum


class User(db.Model):
    __tablename__ = "users"
    id = db.Column( db.Integer, primary_key=True ,autoincrement=True ) #assigns an id as a primary Key
    email = db.Column( db.String, unique = True ) #each email given has to be unique
    password = db.Column(db.String(128)) 
    role=db.Column(db.Boolean , default=False)
    

    def set_password(self):
        hashed_password = bcrypt.generate_password_hash(self.password,10).decode('utf8')
        self.password=hashed_password
    def verify_password(self,password):
        
        return bcrypt.check_password_hash(self.password, password)
    
    
            


    
    











