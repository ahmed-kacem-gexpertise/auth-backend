from app import db , bcrypt
import re
from sqlalchemy.orm import validates



class User(db.Model):
    __tablename__ = "users"
    id = db.Column( db.Integer, primary_key=True ,autoincrement=True ) #assigns an id as a primary Key
    firstName= db.Column( db.String(64) )
    lastName= db.Column( db.String(64) )
    email = db.Column( db.String(64), unique = True ) #each email given has to be unique
    password = db.Column(db.String(128)) 
    role=db.Column(db.Boolean , default=False)

    

    def set_password(self,password):
        hashed_password = bcrypt.generate_password_hash(password,10).decode('utf8')
        self.password=hashed_password
    def verify_password(self,password):
        
        return bcrypt.check_password_hash(self.password, password)
    
    @validates("email")
    def validate_email(self, key, email):
        """Validates the email format before inserting/updating."""
        if not email:
            raise ValueError("Email is required")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email
            


    
    











