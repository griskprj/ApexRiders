from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Member
from datetime import datetime, timezone
from app.utils.admin_required import admin_required
from app.utils.pagination_utils import PaginationService

admin = Blueprint('admin', __name__)

def serializer_user(user):
    """ Сериализация пользователей """
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'admin_level': user.admin_level,
        'is_super_admin': user.is_super_admin,
        'is_verified': user.is_verified,
        'join_at': user.join_at.isoformat() if user.join_at else None,
        'last_admin_login': user.last_admin_login.isoformat() if user.last_admin_login else None,
        'last_login': user.last_login.isoformat() if user.last_login else None,
        'post_count': len(user.posts) if user.posts else 0,
        'product_count': len(user.products) if user.products else 0,
        'manual_count': len(user.authored_manuals) if user.authored_manuals else 0
    }


@admin.route('/users', methods=['GET'])
@jwt_required()
@admin_required(level=5)
def get_users():
    """ Список пользователей """
    try:
        search = request.args.get('search', '')
        admin_level = request.args.get('admin_level', type=int)

        query = Member.query

        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Member.username.ilike(search_filter)) |
                (Member.email.ilike(search_filter))
            )

        if admin_level is not None:
            query = query.filter(Member.admin_level == admin_level)

        query = query.order_by(Member.join_at.desc())

        response_data, status_code = PaginationService.paginate_and_response(
            query=query,
            serializer_func=serializer_user,
            error_out=False
        )

        return jsonify(response_data), status_code

    except Exception as e:
        current_app.logger.error(f'Error getting users list: {str(e)}')
        return jsonify({'error': str(e)}), 500


@admin.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required(level=5)
def delete_user(user_id):
    """ Удаление пользователя """
    try:
        current_user = request.current_user

        if current_user.id == user_id:
            return jsonify({'error': 'Нельзя удалить самого себя'}), 400

        user = Member.query.get(user_id)

        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404

        deleted_data = {
            'username': user.username,
            'email': user.email,
            'deleted_at': datetime.now(timezone.utc).isoformat(),
            'deleted_by': current_user.id
        }

        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'message': 'Пользователь успешно удален',
            'deleted_user': deleted_data
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin.route('/users/<int:user_id>/admin-level', methods=['PUT'])
@jwt_required()
@admin_required(level=5)
def update_admin_level(user_id):
    """ Изменение уровня администратора """
    try:
        data = request.get_json()
        admin_level = data.get('admin_level')

        if int(admin_level) is None or int(admin_level) < 0 or int(admin_level) > 5:
            return jsonify({'error': 'Некорректный уровень администратора'}), 400

        user = Member.query.get(user_id)

        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404

        old_level = user.admin_level
        user.admin_level = admin_level

        if admin_level == 5:
            user.is_super_admin = True
        else:
            user.is_super_admin = False

        user.is_verified = data.get('is_verified')

        db.session.commit()

        return jsonify({
            'message': 'Уровень администратора обновлен',
            'user': {
                'id': user.id,
                'username': user.username,
                'old_admin_level': old_level,
                'new_admin_level': user.admin_level,
                'is_super_admin': user.is_super_admin
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin.route('/stats', methods=['GET'])
@jwt_required()
@admin_required(level=1)
def get_admin_stats():
    """ Статистика админки """
    try:
        user_id = get_jwt_identity()
        user = Member.query.get(user_id)

        total_users = Member.query.count()
        verified_users = Member.query.filter_by(is_verified=True).count()
        admins = Member.query.filter(Member.admin_level > 0).count()
        new_today = Member.query.filter(
            db.func.date(Member.join_at) == datetime.now(timezone.utc).date()
        ).count()

        recent_users = Member.query.order_by(
            Member.join_at.desc()).limit(5).all()
        recent_users_data = [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'join_at': u.join_at.isoformat() if u.join_at else None,
        } for u in recent_users]

        user.last_admin_login = datetime.now(timezone.utc)

        return jsonify({
            'stats': {
                'total_users': total_users,
                'verified_users': verified_users,
                'admin_users': admins,
                'new_today': new_today
            },
            'recent_users': recent_users_data,
            'current_admin': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'admin_level': user.admin_level,
                'is_super_admin': user.is_super_admin,
                'is_verified': user.is_verified,
                'last_admin_login': user.last_admin_login.isoformat(),
                'join_at': user.join_at.isoformat() if user.join_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
