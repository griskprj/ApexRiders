from flask import current_app
from flask_jwt_extended import create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone, timedelta
from app import db
from app.models import Member

class AuthService:
    @staticmethod
    def login(email, password):
        """ Аутентификация пользователя """

        # Проверка входных данных
        if not email:
            return { 'success': False, 'error': 'Почта обязательная' }
        if not password:
            return { 'success': False, 'error': 'Пароль обязателен' }


        # Проверка пользователя
        member = Member.query.filter_by(email=email).first()
        if not member:
            return { 'success': False, 'error': 'Пользователь не найден' }
        if not member.check_password(password):
            return { 'success': False, 'error': 'Неверный пароль' }
        
        # Создаем JWT
        access_token = create_access_token(
            identity=str(member.id),
            expires_delta=timedelta(hours=24)
        )
        
        # Устанавливаем дату последнего входа
        member.last_login = datetime.now(timezone.utc)
        db.session.commit()

        return {
            'success': True,
            'member': member,
            'access_token': access_token,
            'message': 'Вы вошли в систему!'
        }
    
    @staticmethod
    def register(email, username, password):
        """ Регистрация нового пользователя """

        # Проверка существования входных данных
        if not email:
            return {
                'success': False,
                'error': 'Email обязателен',
                'status': 401
            }
        if not username:
            return {
                'success': False,
                'error': 'Имя пользователя обязательно',
                'status': 401
            }
        if not password:
            return {
                'success': False,
                'error': 'Пароль обязателен',
                'status': 401
            }

        # Проверка существования пользователя с полученными данными
        if Member.query.filter_by(email=email).first():
            return {
                'success': False,
                'error': 'Пользователь с такой почтой уже существует',
                'status': 401
            }
        if Member.query.filter_by(username=username).first():
            return {
                'success': False,
                'error': 'Имя пользователя занято',
                'status': 401
            }
        
        # Создание пользователя и токена
        try:
            member = Member(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                admin_level=0,
                join_at=datetime.now(timezone.utc),
                last_login=datetime.now(timezone.utc)
            )
            db.session.add(member)
            db.session.commit()

            return {
                'success': True,
                'member': member,
                'message': 'Регистрация успешна!',
                'status': 201
            }
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Register error: {str(e)}')
            return {
                'success': False,
                'error': 'Ошибка сервера',
                'status': 500
            }
        
    @staticmethod
    def logout():
        """ Выход из аккаунта """
        return {
            'success': True,
            'message': 'Выход из аккаунта произведен',
            'status': 200
        }
    
    @staticmethod
    def get_current_user():
        """ Получить текущего пользователя """
        try:
            current_user_id = get_jwt_identity()

            # Проверка существования пользователя
            user = Member.query.get(current_user_id)
            if not user:
                return {
                    'success': False,
                    'error': 'Пользователь не найден',
                    'status': 404
                }
            
            return {
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'admin_level': user.admin_level
                },
                'status': 200
            }
        
        except Exception as e:
            current_app.logger.error(f'Error getting user: {str(e)}')
            return {
                'success': False,
                'error': 'Ошибка сервера',
                'status': 500
            }