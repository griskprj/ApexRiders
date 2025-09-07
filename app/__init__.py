from flask import Flask, redirect, url_for
from flask_wtf.csrf import CSRFProtect, URLSafeTimedSerializer
from app.extensions import db, migrate, limiter, login_manager, mail
from app.models import User
from app.config import config as cfg
from app.routes.auth import auth
from app.routes.emails import confirmation_reg

serializer = None

def create_app(config_name='default'):
    global serializer

    app = Flask(__name__)
    app_config = cfg[config_name]
    app.config.from_object(app_config)

    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    # Extensions initialize
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'login'

    csfr = CSRFProtect()
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    csfr.init_app(app)
    limiter.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    @login_manager.unauthorized_handler
    def handle_needs_login():
        return redirect(url_for('auth_bp.login'))
    
    app.register_blueprint(auth.auth)
    app.register_blueprint(confirmation_reg.confirmation_reg)
    
    return app
