

import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))





class Config(object):

    """All application configurations"""


    # Secret key

    
    SECRET_KEY=os.getenv('SECRET_KEY')


    # Database configurations
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL') 

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #JWT configurations

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=7)

    JWT_BLACKLIST_TOKEN_CHECKS = ["access","refresh"]
    JWT_TOKEN_LOCATION=['cookies']
    JWT_ACCESS_COOKIE_PATH="/"
    JWT_REFRESH_COOKIE_PATH='/'
    JWT_ACCESS_COOKIE_NAME="access_token"
    JWT_REFRESH_COOKIE_NAME="refresh_token"
    JWT_COOKIE_CSRF_PROTECT=False
    JWT_COOKIE_SECURE=False
    JWT_COOKIE_SAMESITE= "None" 
    SWAGGER_UI_CONFIG={
    "withCredentials": True  # Allows Swagger to send cookies with requests
    }
    JWT_COOKIE_DOMAIN ="127.0.0.1"
    #mail configurations

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587  #  587 for TLS or 465 for SSL
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False  #  True if using SSL (port 465)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  #  App Password for Gmail 
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')  # Default sender address 

    #frontend base url
    BASE_URL="http://127.0.0.1:3000"

    