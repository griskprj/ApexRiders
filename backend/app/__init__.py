import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import datetime

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return jsonify({'error': 'Missing authorization token'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify({'erorr': 'Invalid token'}), 422

@jwt.expired_token_loader
def expired_token_loader(jwt_header, jwt_payload):
    return jsonify({'error': 'Token has expired'}), 401

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://apexuser:8sE>HVx#~#*p;UM0D3LZ@localhost/apexriders'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'secretKeyChangeToProduct'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=24)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    db.init_app(app)
    jwt.init_app(app)
    migrate(app, db, render_as_batch=True)
    CORS(app, resources={
        r"/api/*": {
            "origins": ["https://yourdomot.ru", "http://yourdomot.ru", "http://80.78.242.175"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type"]
        }
    })

    from app.routes import auth, motorcycles, statist, manuals, courses, product, community, garage
    app.register_blueprint(auth.auth)
    app.register_blueprint(motorcycles.motorcycle)
    app.register_blueprint(statist.statistic)
    app.register_blueprint(manuals.manuals)
    app.register_blueprint(product.product)
    app.register_blueprint(courses.courses)
    app.register_blueprint(community.community)
    app.register_blueprint(garage.garage)

    with app.app_context():
        db.create_all()

    return app