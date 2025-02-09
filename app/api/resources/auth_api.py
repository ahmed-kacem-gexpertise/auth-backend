from flask_restx import Namespace, Resource, fields
from flask import request
from marshmallow import ValidationError
from ..api_schemas import RegisterUserSchema
from ..services.user_service import add_user
    
from ..api_schemas import LoginUserSchema
from ..services.auth_service import authenticate
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
@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        try:
            data = user_schema.load(request.json)
            access_token = authenticate(data["email"], data["password"])
            if access_token:
                return {"access_token": access_token}, 200
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
                return {"msg": "user created successfuly"},200
            else:
                return {"error":"user already exists"},401
        except ValidationError as err :
            return {"errors": err.messages}, 400