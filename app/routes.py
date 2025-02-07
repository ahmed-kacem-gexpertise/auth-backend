

from app import app, db , bcrypt




from app.models import User

from flask import  request, jsonify, session,flash

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt
@app.route('/')
@jwt_required(optional=True)
def home():
    claims = get_jwt()
    user_identity=get_jwt_identity()
    if claims:
        return jsonify(logged_in_as=user_identity,id=claims['role'])
    else:
        return jsonify(logged_in_as="anonymous user")



#Using an `after_request` callback, we refresh any token that is within 30 mins
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response



@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()
    
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401
    #checking if the password is the same as hashed password
    if not user.verify_password(password):
        return jsonify({"error": "Unauthorized"}), 401
    
    additional_claims = {"role": user.role}
    access_token = create_access_token(identity=email,additional_claims=additional_claims)
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
    new_user = User(email=email, role=False)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    
    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })


@app.route("/userProfile",methods=["GET"])
@jwt_required()
def user_info():
    
    user_identity=get_jwt_identity()
    user_info= User.query.filter_by(email=user_identity).first()
    return jsonify(email=user_info.email , role=user_info.role )

@app.route("/changeUserPassword",methods=["POST"])
@jwt_required()
def change_passowrd():
    old_password=request.json['old_password']
    new_password=request.json['new_password']
    user_identity=get_jwt_identity()
    user= User.query.filter_by(email=user_identity).first()
    if old_password != new_password and user.verify_password(old_password):
        user.set_password()
        db.session.commit()
        return jsonify({"msg":"password changed successfuly","state":True})
    return jsonify({"msg":"verify your credentials","state":False})
        