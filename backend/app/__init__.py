from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import datetime

db = SQLAlchemy()
jwt = JWTManager()

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'secretKeyChangeToProduct'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=24)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=['http://localhost:3000'], supports_credentials=True)

    from app.routes import auth, motorcycles, statist, manuals
    app.register_blueprint(auth.auth)
    app.register_blueprint(motorcycles.motorcycle)
    app.register_blueprint(statist.statistic)
    app.register_blueprint(manuals.manuals)

    with app.app_context():
        db.create_all()

    return app