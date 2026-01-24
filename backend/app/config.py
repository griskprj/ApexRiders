import os
from datetime import timedelta
from dotenv import load_dotenv

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_ACCESS_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    UPLOAD_URL_PATH = '/uploads'
    
    @staticmethod
    def init_app(app):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    JWT_SECRET_KEY = 'dev-secret-key-change-this'
    CORS_ORIGINS = ['http://localhost:8080', 'http://localhost:3000']
    
    @staticmethod
    def init_app(app):
        super(DevelopmentConfig, DevelopmentConfig).init_app(app)

class ProductionConfig(Config):
    env_file = '.env.production' if os.path.exists('.env.production') else '.env.development'
    load_dotenv(env_file)
    
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or os.environ.get('DATABASE_URI')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fallback-secret-key')
    
    CORS_ORIGINS = []
    cors_env = os.environ.get('CORS_ORIGINS')
    if cors_env:
        CORS_ORIGINS = [origin.strip() for origin in cors_env.split(',') if origin.strip()]
    
    @staticmethod
    def init_app(app):
        super(ProductionConfig, ProductionConfig).init_app(app)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}