

from app import app, db , bcrypt




from app.models import User

from flask import  request, jsonify, session,flash






@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API"})








@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()
    
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401
    #checking if the password is the same as hashed password
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    
    return jsonify({
        "id": user.id,
        "email": user.email
    })






@app.route("/register", methods=["POST"])
def register_user():
    #gets email and password input
    email = request.json["email"]
    password = request.json["password"]

   
    hashed_password = bcrypt.generate_password_hash(password,10).decode('utf8')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    
    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })





