

from app import app, db , bcrypt




from app.models import User

from flask import  request, jsonify, session,flash




from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


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
    
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200





@app.route("/register", methods=["POST"])
def register_user():
    #gets email and password input
    email = request.json["email"]
    password = request.json["password"]

    if User.query.filter_by(email=email).first() :
        return jsonify({"error": "email already exists"}), 403
    hashed_password = bcrypt.generate_password_hash(password,10).decode('utf8')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    
    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })





