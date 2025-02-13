from marshmallow import Schema, fields, validate


class LoginUserSchema(Schema):
    email = fields.Email(
        required=True,
        validate=validate.Length(max=100),  # Limit email length
        error_messages={"invalid": "Please provide a valid email address"}
    )
    password = fields.String(required=True)
    rememberMe = fields.Boolean(default=False, description="Remember Me option")
class RegisterUserSchema(Schema):
    email = fields.Email(
        required=True,
        validate=validate.Length(max=100),  # Limit email length
        error_messages={"invalid": "Please provide a valid email address"}
    )
    password = fields.String(required=True)
    firstName = fields.String(required=True)
    lastName = fields.String(required=True)
class UpdateUserSchema(Schema):
    email = fields.Email(
        required=False,
        validate=validate.Length(max=100),  # Limit email length
        error_messages={"invalid": "Please provide a valid email address"}
    )
    firstName = fields.String(required=False)
    lastName = fields.String(required=False)

