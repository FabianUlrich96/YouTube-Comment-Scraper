import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4'.format(
    os.getenv('DB_USER', 'dataapi'),
    os.getenv('DB_PASSWORD', 'fnmwm4d833834erjn'),
    os.getenv('DB_HOST', 'dataapidb'),
    os.getenv('DB_NAME', 'dataapi'),
)
app.config["JWT_SECRET_KEY"] = "sdadaji3u2h3u4h23u42334234kdas"

jwt = JWTManager(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)










