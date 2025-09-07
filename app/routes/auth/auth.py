from flask import Blueprint, redirect, url_for, render_template, jsonify, flash, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, limiter
from app.models import User
from app.utils.photo import get_photo
from app.utils.emails.register import send_register_confirmation_email

CONFIRMATION_EXPIRATION = 3600

auth = Blueprint('auth', __name__, url_prefix='/auth')

""" LOGIN """
@auth.route('/login', methods=['POST', 'GET'])
@limiter.limit('5 per minute')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember-me') == 'on'

        if not username or not password:
            flash('Заполните все поля', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Неверные учетные данные', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_confirmed:
            flash('Подтвердите email перед входом', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        flash('Вы успешно вошли', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('/auth/login.html')

""" REGISTER """
@auth.route('/register', methods=['POST', 'GET'])
@limiter.limit('5 per minute')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([username, email, password]):
            flash('Заполните все поля', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            flash('Имя пользователя занято', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email уже зарегистрирован', 'danger')
            return redirect(url_for('auth.register'))
        
        try:
            user = User(
                username=username,
                email=email,
                password=generate_password_hash(password),
                is_confirmed=False
            )

            db.session.add(user)
            db.session.commit()

            send_register_confirmation_email(user)

            flash('Регистрация успешна. Проверьте вашу почту для подтверждения email', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error registration: {e}')
            flash('Ошибка регистрации. Повторите попытку позднее', 'danger')

    return render_template('/auth/register.html')

""" LOGOUT """
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('main.index'))

""" USER AVATAR """
@auth.route('/user_image:<int:user_id>')
@login_required
def user_image(user_id):
    user = User.query.get_or_404(user_id)

    return get_photo(user)

