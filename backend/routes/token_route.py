from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token
from app_config import db
from database.models import Users
import logger

log = logger.create_logger(__name__)

token_blueprint = Blueprint('token_blueprint', __name__, template_folder='templates')


@token_blueprint.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    exists = db.session.query(Users).filter(Users.username == username, Users.password == password).first() is not None
    if not exists:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

