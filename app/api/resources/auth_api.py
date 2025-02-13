from flask_restx import Namespace, Resource, fields
from flask import request,jsonify
from marshmallow import ValidationError
from ..api_schemas import RegisterUserSchema
from ..services.user_service import add_user
from flask_jwt_extended import get_jwt_identity ,create_access_token,set_access_cookies,jwt_required
from ..api_schemas import LoginUserSchema
from ..services.auth_service import authenticate ,confirm_user_email,check_user_exists
from ...extensions import email_service
register_user_schema = RegisterUserSchema()
auth_ns = Namespace("auth", description="Authentication API")

user_schema=LoginUserSchema()
register_model=auth_ns.model(
    "register",
    {  
        "firstName":fields.String(required=True, description="User's firstName"),
        "lastName":fields.String(required=True, description="User's lastName"),
        "email": fields.String(required=True, description="User's email",example="example@gmail.com"),
        "password": fields.String(required=True, description="User's password"),

    },
    )
login_model = auth_ns.model(
    "Login",
    {
        "email": fields.String(required=True, description="User's email",example="example@gmail.com"),
        "password": fields.String(required=True, description="User's password"),
    },
)
reset_password_model=auth_ns.model(
    "reset password",
    {
        "new_password":fields.String(required=True, description="User's new password"),
    },
)
forgot_password_model=auth_ns.model(
    "forgot password",
    {
        "email": fields.String(required=True, description="User's email",example="example@gmail.com"),
    },
)
@auth_ns.route("/token/refresh")
class RefreshToken(Resource):
    @auth_ns.doc(description="Refresh access token using the refresh token stored in cookies.")

    @jwt_required(refresh=True) 
    def post(self):
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)  
            
            resp = jsonify({'refresh': True})  
            set_access_cookies(resp, access_token)  
            return resp  
        except Exception as e:
            return {"error":e}
@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        try:
            data = user_schema.load(request.json)
            resp = authenticate(data["email"], data["password"])
            if resp:
                return resp
            return {"message": "Invalid credentials"}, 401
        except ValidationError as err:
            return {"errors": err.messages}, 400
@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(register_model)
    def post(self):
        try:
            data=register_user_schema.load(request.json)
            is_user_created=add_user(data)
            if is_user_created : 
                email_service.send_confirmation_email(data["email"])

                return {"message": "Registration successful, please check your email to confirm."}, 201
            else:
                return {"error":"user already exists"},401
        except ValidationError as err :
            return {"errors": err.messages}, 400
@auth_ns.route("/confirm/<token>")
class Confirm(Resource):
    def post(self,token):
        try:
            email = email_service.serializer.loads(token, salt='email-confirm', max_age=3600)  # Token expires after 1 hour
        except Exception as e:
            return {"message": "The confirmation link is invalid or has expired.",'error':e.message}, 400
        user=confirm_user_email(email)
        if user:
            return {"message": "Your email has been confirmed!"}, 200
        
        else:
            return {"message": "User not found."}, 404
@auth_ns.route("/forgot_password")
class ForgotPassword(Resource):
    @auth_ns.expect(forgot_password_model)
    
    def post (self):
        data = request.get_json()
        email = data.get("email")

        user = check_user_exists(email)
        if not user:
            return {"message": "No user with that email."}, 404
        try:
            email_service.send_password_reset_email(email)
            return {"message": "Password reset email has been sent!"}, 200
        except Exception as e :
            return {"error": "there was an error sending the reset password email please try again "},401
@auth_ns.route("/resetPassword/<token>")
class Reset(Resource):
    @auth_ns.expect(reset_password_model)
    
    def post (self,token):
        try:
            email = email_service.serializer.loads(token, salt='password-reset', max_age=900)  
        except Exception as e:
            return {"message": "The reset link is invalid or has expired."}, 400

        user = check_user_exists(email)
        if not user:
            return {"message": "User not found."}, 404

        # Assuming you pass the new password in the request body
        data = request.get_json()
        new_password = data.get("new_password")
        user.set_password(new_password)
        
        return {"message": "Your password has been reset successfully!"}, 200
