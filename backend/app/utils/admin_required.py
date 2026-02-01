from flask import request, jsonify
from functools import wraps
from app.models import Member
from flask_jwt_extended import get_jwt_identity

def admin_required(level=1):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                current_user_id = get_jwt_identity()
                
                user = Member.query.get(current_user_id)

                if user.admin_level == 0 and not user.is_super_admin:
                    return jsonify({
                        'error': 'Требуются права администратора',
                        'code': 'NOT_ADMIN'
                    }), 403
                
                if user.admin_level < level and not user.is_super_admin:
                    return jsonify({
                        'error': f'Требуется уровень администрирования {level} или выше',
                    }), 403
                
                request.current_user = user
                
                return fn(*args, **kwargs)
                
            except Exception as e:
                return jsonify({
                    'error': 'Недействительный токен',
                    'details': str(e),
                }), 401
                
        return decorator
    return wrapper