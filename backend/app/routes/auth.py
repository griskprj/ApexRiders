import os
from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import (
    Member,
    Post,
    Like,
    Comment,
    Motorcycle,
    MotorcycleMaintenance,
    MotorcycleNote,
    ManualRating,
    ManualDraft,
    UserManualProgress,
    UserManualHistory,
    UserLessonHistory,
    UserCoursesHistory,
    Product
)
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from app.services.auth_service import AuthService

auth = Blueprint('auth', __name__)


@auth.route('/api/auth/login', methods=['POST'])
def login_user():
    """ Аутентификация пользователя """
    data = request.get_json()

    result = AuthService.login(
        email=data.get('email'),
        password=data.get('password')
    )

    return jsonify({
        'access_token': result['access_token'],
        'member': {
            'id': result['member'].id,
            'username': result['member'].username,
            'email': result['member'].email,
            'admin_level': result['member'].admin_level,
            'is_super_admin': result['member'].is_super_admin,
            'is_verified': result['member'].is_verified
        },
        'message': result['message']
    })


@auth.route('/api/auth/register', methods=['POST'])
def register_user():
    """ Регистрация пользователя """
    data = request.get_json()
    
    result = AuthService.register(
        email=data.get('email'),
        username=data.get('username'),
        password=data.get('password')
    )

    return jsonify({
        'user': {
            'id': result['member'].id,
            'username': result['member'].username,
            'email': result['member'].email
        },
        'message': result['message']
    }), 201


@auth.route('/api/auth/user', methods=['GET'])
@jwt_required()
def get_current_user():
    """ Получить текущего пользователя """
    result = AuthService.get_current_user()

    return jsonify({
        'user': result['user']
    })


@auth.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout_user():
    """ Выход из аккаунта """
    result = AuthService.logout()
    return jsonify({
        'message': result['message']
    })


@auth.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """ GET PROFILE """
    user_id = get_jwt_identity()
    user = Member.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'join_at': user.join_at.isoformat() if user.join_at else None,
        'is_verified': user.is_verified,
        'verification_data': user.verification_date.isoformat() if user.verification_date else None
    })


@auth.route('/api/auth/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """ UPDATE PROFILE """
    user_id = get_jwt_identity()
    user = Member.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    if 'username' in data:
        existing_user = Member.query.filter(
            Member.username == data['username'],
            Member.id != user_id
        ).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400
        user.username = data['username']

    if 'email' in data:
        existing_user = Member.query.filter(
            Member.email == data['email'],
            Member.id != user_id
        ).first()
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 400
        user.email = data['email']

    db.session.commit()

    return jsonify({
        'id': user.id,
        'usename': user.username,
        'email': user.email,
        'role': user.role,
        'join_at': user.join_at.isoformat() if user.join_at else None
    })


@auth.route('/api/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """ CHANGE-PASSWORD """
    user_id = get_jwt_identity()
    user = Member.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_password or not new_password:
        return jsonify({'error': 'Current and new password required'}), 400

    if not user.check_password(current_password):
        return jsonify({'error': 'Current password is incorrect'}), 400

    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Password updated successfully'})


@auth.route('/api/auth/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    """ DELETE ACCOUNT """
    try:
        current_user_id = get_jwt_identity()

        user = Member.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404

        posts = Post.query.filter_by(author_id=current_user_id).all()
        for post in posts:
            if post.image_filename:
                try:
                    upload_dir = os.path.join(current_app.config.get(
                        'UPLOAD_FOLDER', 'static/uploads'), 'posts')
                    image_path = os.path.join(upload_dir, post.image_filename)
                    if os.path.exists(image_path):
                        os.remove(image_path)
                        current_app.logger.info(
                            f'Deleted post image: {image_path}')
                except Exception as e:
                    current_app.logger.error(
                        f'Error deleting post image: {str(e)}')

            comments = Comment.query.filter_by(post_id=post.id).all()
            for comment in comments:
                comment_likes = Like.query.filter_by(
                    target_type='comment', target_id=comment.id).all()
                for like in comment_likes:
                    db.session.delete(like)
                db.session.delete(comment)

            post_likes = Like.query.filter_by(
                target_type='post', target_id=post.id).all()
            for like in post_likes:
                db.session.delete(like)

            db.session.delete(post)

        user_comments = Comment.query.filter_by(
            author_id=current_user_id).all()
        for comment in user_comments:
            comment_likes = Like.query.filter_by(
                target_type='comment', target_id=comment.id).all()
            for like in comment_likes:
                db.session.delete(like)
            db.session.delete(comment)

        user_likes = Like.query.filter_by(user_id=current_user_id).all()
        for like in user_likes:
            db.session.delete(like)

        motorcycles = Motorcycle.query.filter_by(user_id=current_user_id).all()
        for motorcycle in motorcycles:
            notes = MotorcycleNote.query.filter_by(
                motorcycle_id=motorcycle.id).all()
            for note in notes:
                db.session.delete(note)

            maintenance_tasks = MotorcycleMaintenance.query.filter_by(
                motorcycle_id=motorcycle.id).all()
            for task in maintenance_tasks:
                db.session.delete(task)

            db.session.delete(motorcycle)

        manual_progress = UserManualProgress.query.filter_by(
            user_id=current_user_id).all()
        for progress in manual_progress:
            db.session.delete(progress)

        manual_ratings = ManualRating.query.filter_by(
            user_id=current_user_id).all()
        for rating in manual_ratings:
            db.session.delete(rating)

        manual_history = UserManualHistory.query.filter_by(
            user_id=current_user_id).all()
        for history in manual_history:
            db.session.delete(history)

        lesson_history = UserLessonHistory.query.filter_by(
            user_id=current_user_id).all()
        for history in lesson_history:
            db.session.delete(history)

        courses_history = UserCoursesHistory.query.filter_by(
            user_id=current_user_id).all()
        for history in courses_history:
            db.session.delete(history)

        manual_drafts = ManualDraft.query.filter_by(
            user_id=current_user_id).all()
        for draft in manual_drafts:
            if draft.uploaded_images:
                try:
                    upload_dir = os.path.join(current_app.config.get(
                        'UPLOAD_FOLDER', 'static/uploads'), 'manuals')
                    for image_name in draft.uploaded_images:
                        image_path = os.path.join(upload_dir, image_name)
                        if os.path.exists(image_path):
                            os.remove(image_path)
                except Exception as e:
                    current_app.logger.error(
                        f'Error deleting draft images: {str(e)}')
            db.session.delete(draft)

        products = Product.query.filter_by(owner_id=current_user_id).all()
        for product in products:
            product_likes = Like.query.filter_by(
                target_type='product',
                target_id=product.id
            ).all()
            for like in product_likes:
                db.session.delete(like)

            db.session.delete(product)

        db.session.delete(user)
        db.session.commit()

        current_app.logger.info(f'Account deleted: user_id={current_user_id}')

        return jsonify({
            'success': True,
            'message': 'Аккаунт успешно удален'
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error deleting account: {str(e)}')
        return jsonify({'error': 'Ошибка при удалении аккаунта'}), 500
