from ..extensions import db , bcrypt

from sqlalchemy.orm import validates



class User(db.Model):
    __tablename__ = "users"
    id = db.Column( db.Integer, primary_key=True ,autoincrement=True ) #assigns an id as a primary Key
    firstName= db.Column( db.String(64) )
    lastName= db.Column( db.String(64) )
    email = db.Column( db.String(64), unique = True ) #each email given has to be unique
    password = db.Column(db.String(128)) 
    admin=db.Column(db.Boolean , default=False)
    is_confirmed=db.Column(db.Boolean , default=False)


    

    def set_password(self,password):
        hashed_password = bcrypt.generate_password_hash(password,10).decode('utf8')
        self.password=hashed_password
        db.session.commit()

    def verify_password(self,password):
        return bcrypt.check_password_hash(self.password, password)
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    def update_info(self,**kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:  
                setattr(self, key, value)
        db.session.commit()
    def confirm_user(self):
        self.is_confirmed=True
        db.session.commit()
    



   


    
    











