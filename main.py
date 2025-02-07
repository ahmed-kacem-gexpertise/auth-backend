from app import app,db,create_databases

from flask_cors import CORS

CORS(app, supports_credentials=True)


if __name__ == '__main__':
    create_databases()

    app.run(port=5555, debug=True)