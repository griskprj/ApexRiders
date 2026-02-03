from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Notification, Member, Post, Comment, Product
from datetime import datetime, timezone

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """ Get notifications """
    try:
        user_id = get_jwt_identity()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        unread_only = request.args.get(
            'unread_only', 'false').lower() == 'true'
        notification_type = request.args.get('type')

        query = Notification.query.filter_by(
            user_id=user_id, is_archived=False)

        if unread_only:
            query = query.filter_by(is_read=False)

        if notification_type:
            query = query.filter_by(notification_type=notification_type)

        query = query.order_by(Notification.created_at.desc())

        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False)

        notifications = [n.to_dict() for n in pagination.items]

        unread_count = Notification.query.filter_by(
            user_id=user_id,
            is_read=False,
            is_archived=False
        ).count()

        return jsonify({
            'notifications': notifications,
            'unread_count': unread_count,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200

    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': str(e)}), 500


@notifications_bp.route('/notifications/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notification_id):
    """ Mark notification as read """
    try:
        user_id = get_jwt_identity()

        notification = Notification.query.get_or_404(notification_id)

        if int(notification.user_id) != int(user_id):
            return jsonify({'error': 'Недостаточно прав'}), 403

        notification.mark_as_read()
        db.session.commit()

        return jsonify({
            'message': 'Сообщение отмечено как прочитанное',
            'notification': notification.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e)
        }), 500


@notifications_bp.route('/notifications/read-all', methods=['PUT'])
@jwt_required()
def make_all_read():
    """ Mark all notifications as read """
    try:
        user_id = get_jwt_identity()

        notifications = Notification.query.filter_by(
            user_id=user_id,
            is_read=False,
            is_archived=False
        ).all()

        now = datetime.now(timezone.utc)
        for notification in notifications:
            notification.is_read = True
            notification.read_at = now

        db.session.commit()

        return jsonify({
            'message': f'Все уведомления {len(notifications)} отмечены как прочитанные'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e)
        }), 500


@notifications_bp.route('/notifications/<int:notification_id>/archive', methods=['PUT'])
@jwt_required()
def archive_notification(notification_id):
    """ Move notification to archive """
    try:
        user_id = get_jwt_identity()

        notification = Notification.query.get_or_404(notification_id)

        if int(notification.user_id) != int(user_id):
            return jsonify({'error': 'Недостаточно прав'}), 403

        notification.is_archived = True
        db.session.commit()

        return jsonify({
            'message': 'Уведомление перемещено в архив'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e)
        }), 500


@notifications_bp.route('/notifications/count', methods=['GET'])
@jwt_required()
def get_notifications_count():
    """ Get notifications count """
    try:
        user_id = get_jwt_identity()

        unread_count = Notification.query.filter_by(
            user_id=user_id,
            is_read=False,
            is_archived=False
        ).count()

        return jsonify({
            'unread_count': unread_count
        })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@notifications_bp.route('/admin/send-notification', methods=['POST'])
@jwt_required()
def send_admin_notification():
    """ Send admin notification """
    try:
        current_user_id = get_jwt_identity()
        current_user = Member.query.get(current_user_id)

        if current_user.admin_level == 0 and not current_user.is_super_admin:
            return jsonify({'error': 'Недостаточно прав'}), 403

        data = request.get_json()

        user_id = data.get('user_id')
        title = data.get('title')
        message = data.get('message')
        notification_type = data.get('type', 'admin_broadcast')
        priority = data.get('priority', 'normal')

        if not user_id or not title:
            return jsonify({'error': 'Не все обязательные поля заполнены'}), 400

        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            target_type='admin',
            priority=priority,
            admin_id=current_user_id
        )

        db.session.add(notification)
        db.session.commit()

        return jsonify({
            'message': 'Уведомление отправлено успешно',
            'notification': notification.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'erorr': str(e)
        }), 500


@notifications_bp.route('/admin/send-report', methods=['POST'])
@jwt_required()
def send_admin_report():
    """ Send admin report to user """
    try:
        current_user_id = get_jwt_identity()
        current_user = Member.query.get(current_user_id)

        if current_user.admin_level == 0 and not current_user.is_super_admin:
            return jsonify({'error': 'Недостаточно прав'}), 403

        data = request.get_json()

        user_id = data.get('user_id')
        target_type = data.get('target_type')
        target_id = data.get('target_id')
        reason = data.get('reason')
        action_taken = data.get('action_taken')

        if not user_id or not target_type or not reason:
            return jsonify({'error': 'Заполните обязательные поля'}), 400

        target_info = {}
        if target_type == 'post':
            post = Post.query.get(target_id)
            if post:
                target_info = {
                    'post_title': post.title,
                    'author': post.author.username
                }
        elif target_type == 'comment':
            comment = Comment.query.get(target_id)
            if comment:
                target_info = {
                    'comment_content': comment.comment[:100],
                    'author': comment.author.username
                }
        elif target_type == 'product':
            product = Product.query.get(target_id)
            if product:
                target_info = {
                    'product_title': product.title[:100],
                    'owner': product.owner.username
                }

        notification = Notification(
            user_id=user_id,
            notification_type='admin_report',
            title='Жалоба на контент',
            message=f'Администратор оставил жалобу на ваш {target_type}. Причина: {reason}. {f"Принятые меры: {action_taken}" if action_taken else ""}',
            target_type=target_type,
            target_id=target_id,
            priority='high',
            admin_id=current_user_id,
            metadata={
                'reason': reason,
                'action_taken': action_taken,
                'target_info': target_info,
            }
        )

        db.session.add(notification)
        db.session.commit()

        return jsonify({
            'message': 'Жалоба отправлена пользователю',
            'notification': notification.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e)
        }), 500
