from dotenv import load_dotenv
import  os 

load_dotenv()
class CoolConfig(object):
    SQLALCHEMY_DATABASE_URI =  os.getenv('DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False