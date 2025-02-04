from flask import Flask
from flask import Blueprint

blueprint = Blueprint('user',__name__, url_prefix= '/bye')
app = Flask(__name__)
@blueprint.route("/user")