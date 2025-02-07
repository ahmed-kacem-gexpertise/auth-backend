from app import app
from app.setup import create_databases
from flask_cors import CORS

CORS(app, supports_credentials=True)


if __name__ == '__main__':
    

    app.run(port=5555, debug=True)