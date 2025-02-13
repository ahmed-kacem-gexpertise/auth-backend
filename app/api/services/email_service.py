from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

from flask_mail import Mail
mail= Mail()
class EmailService:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        mail.init_app(app)
        self.serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    def send_confirmation_email(self, user_email):
        """Generate a confirmation link and send it to the user email."""
        token = self.serializer.dumps(user_email, salt='email-confirm')
        confirm_url = f"{current_app.config['BASE_URL']}/confirm/{token}"

        msg = Message("Please Confirm Your Email Address", recipients=[user_email])
        msg.body = f"Click the link to confirm your email: {confirm_url}"
        mail.send(msg)

    def send_password_reset_email(self, user_email):
        """Generate a password reset link and send it to the user email."""
        token = self.serializer.dumps(user_email, salt='password-reset')
        reset_url = f"{current_app.config['BASE_URL']}/reset_password/{token}"

        msg = Message("Password Reset Request", recipients=[user_email])
        msg.body = f"Click the link to reset your password: {reset_url}"
        mail.send(msg)