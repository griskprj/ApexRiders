import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .config import config
from dotenv import load_dotenv

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return jsonify({'error': 'Missing authorization token'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify({'error': 'Invalid token'}), 422

@jwt.expired_token_loader
def expired_token_loader(jwt_header, jwt_payload):
    return jsonify({'error': 'Token has expired'}), 401

def create_app(config_name=None):
    app = Flask(__name__)

    # Определяет конфиг
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    if config_name not in config:
        config_name = 'default'

    app.config.from_object(config[config_name])
    app.config['ENV'] = config_name

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    config[config_name].init_app(app)
    
    # Настройка CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type"],
            "supports_credentials": True
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

    if app.config['DEBUG']:
        with app.app_context():
            db.create_all()

    return app