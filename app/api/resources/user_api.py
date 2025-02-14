from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
from ..services.user_service import get_user_info,update_user,change_user_password
from ..api_schemas import UpdateUserSchema
from marshmallow import ValidationError

register_user_schema=UpdateUserSchema()

user_ns = Namespace("user", description="user CRUD API")
parser = reqparse.RequestParser()
parser.add_argument('id', type=str, required=True, help="user id")
user_info_model=user_ns.model(
    "userInfo",
    {  
        "firstName":fields.String(required=True, description="User's firstName"),
        "lastName":fields.String(required=True, description="User's lastName"),
        "email": fields.String(required=True, description="User's email",example="example@gmail.com"),

    },
    )
change_user_info_model = user_ns.model(
    "ChangeUserInfo",
    {  
        "firstName":fields.String(required=False, description="User's firstName"),
        "lastName":fields.String(required=False, description="User's lastName"),
        "email": fields.String(required=False, description="User's email",example="example@gmail.com"),
    }
)
change_user_password_model= user_ns.model(
    "ChangePassword",
    {
        "old_password":fields.String(required=True , description="User's old Password"),
        "new_password":fields.String(required=True, description="User's new Password"),

    }
)
@user_ns.route("/profile")
class UserResource(Resource):
    
    @jwt_required()
    @user_ns.marshal_with(user_info_model)
    @user_ns.expect(parser)
    def get (self):
        args = parser.parse_args()  
        user_id = args['id']
        user_info=get_user_info(user_id)
        
        return user_info
    @jwt_required()
    @user_ns.expect(change_user_info_model,parser)
    def put(self):
        args = parser.parse_args()  
        user_id = args['id']
        try:
            data=register_user_schema.load(request.json)
            if not data:
                return {"msg":"no changes were made "}
            updated = update_user(data,user_id)
            if updated : 
                return {"msg":"user updated successfuly"},200
            return {
                "error": "there was an error updating the info "
            }
        
        except ValidationError as err:
            return {"errors": err.messages}, 400
@user_ns.route("/changePassword")
class ChangeUserPassword(Resource):
    
    @jwt_required()
    @user_ns.expect(change_user_password_model)
    def put(self):
        data=request.json
        changedPassword=change_user_password(data)
        if changedPassword:
            return {"msg":"password changed successfuly"},200
        return {"error":"invalid credentials"}

