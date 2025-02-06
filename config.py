

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
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)
   
    