from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Report, Member, Post, Comment, Product, MaintenanceManual
from datetime import datetime, timezone
from app.utils.admin_required import admin_required
from app.services.notification_service import NotificationService

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports', methods=['GET'])
@jwt_required()
@admin_required(level=4)
def get_reports():
    """Получить список жалоб с фильтрацией"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', 'pending')
        priority = request.args.get('priority')
        target_type = request.args.get('target_type')
        assigned_to_me = request.args.get('assigned_to_me', 'false').lower() == 'true'
        
        current_user_id = get_jwt_identity()
        
        query = Report.query
        
        # Фильтрация по статусу
        if status != 'all':
            query = query.filter(Report.status == status)
        
        # Фильтрация по приоритету
        if priority:
            query = query.filter(Report.priority == priority)
        
        # Фильтрация по типу цели
        if target_type:
            query = query.filter(Report.target_type == target_type)
        
        # Фильтрация по назначенному модератору
        if assigned_to_me:
            query = query.filter(Report.assigned_admin_id == current_user_id)
        elif assigned_to_me is False:
            query = query.filter((Report.assigned_admin_id.is_(None)) | 
                                (Report.assigned_admin_id != current_user_id))
        
        # Сортировка
        query = query.order_by(
            Report.priority.desc(), 
            Report.created_at.desc()
        )
        
        # Пагинация
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        reports = []
        for report in pagination.items:
            reports.append(report.to_dict(include_details=False))
        
        # Статистика
        stats = {
            'total': Report.query.count(),
            'pending': Report.query.filter_by(status='pending').count(),
            'reviewing': Report.query.filter_by(status='reviewing').count(),
            'resolved': Report.query.filter_by(status='resolved').count(),
            'assigned_to_me': Report.query.filter_by(
                assigned_admin_id=current_user_id,
                status='reviewing'
            ).count()
        }
        
        return jsonify({
            'reports': reports,
            'stats': stats,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/reports/<int:report_id>', methods=['GET'])
@jwt_required()
@admin_required(level=4)
def get_report_detail(report_id):
    """Получить детальную информацию о жалобе"""
    try:
        report = Report.query.get_or_404(report_id)
        
        return jsonify({
            'report': report.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/reports/<int:report_id>/assign', methods=['POST'])
@jwt_required()
@admin_required(level=4)
def assign_report(report_id):
    """Назначить жалобу себе на проверку"""
    try:
        current_user_id = get_jwt_identity()
        report = Report.query.get_or_404(report_id)
        
        if report.assigned_admin_id and report.assigned_admin_id != current_user_id:
            return jsonify({'error': 'Жалоба уже назначена другому модератору'}), 400
        
        report.assigned_admin_id = current_user_id
        report.status = 'reviewing'
        report.updated_at = datetime.now(timezone.utc)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Жалоба назначена вам на проверку',
            'report': report.to_dict(include_details=False)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/reports/<int:report_id>/resolve', methods=['POST'])
@jwt_required()
@admin_required(level=4)
def resolve_report(report_id):
    """Завершить обработку жалобы"""
    try:
        data = request.get_json()
        report = Report.query.get_or_404(report_id)
        
        current_user_id = get_jwt_identity()
        
        # Проверяем, что жалоба назначена текущему пользователю
        if int(report.assigned_admin_id) != int(current_user_id):
            return jsonify({'error': 'Вы не назначены на эту жалобу'}), 403
        
        resolution = data.get('resolution')
        resolution_type = data.get('resolution_type')
        
        if not resolution or not resolution_type:
            return jsonify({'error': 'Необходимо указать решение и тип'}), 400
        
        # Обновляем статус жалобы
        report.status = 'resolved'
        report.resolution = resolution
        report.resolution_type = resolution_type
        report.resolved_at = datetime.now(timezone.utc)
        report.updated_at = datetime.now(timezone.utc)
        
        # Отправляем уведомление пользователю, на которого пожаловались
        if report.reported_user_id:
            try:
                NotificationService.send_admin_report(
                    user_id=report.reported_user_id,
                    admin_id=current_user_id,
                    target_type=report.target_type,
                    target_id=report.target_id,
                    reason=report.reason,
                    action_taken=resolution
                )
            except Exception as e:
                print(f"Error sending notification: {e}")
                # Продолжаем выполнение даже если уведомление не отправилось
        
        db.session.commit()
        
        return jsonify({
            'message': 'Жалоба успешно обработана',
            'report': report.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/reports/<int:report_id>/dismiss', methods=['POST'])
@jwt_required()
@admin_required(level=4)
def dismiss_report(report_id):
    """Отклонить жалобу"""
    try:
        data = request.get_json()
        report = Report.query.get_or_404(report_id)
        
        current_user_id = get_jwt_identity()
        
        # Проверяем, что жалоба назначена текущему пользователю
        if report.assigned_admin_id != current_user_id:
            return jsonify({'error': 'Вы не назначены на эту жалобу'}), 403
        
        resolution = data.get('resolution', 'Жалоба отклонена как необоснованная')
        
        report.status = 'dismissed'
        report.resolution = resolution
        report.resolution_type = 'dismissed'
        report.resolved_at = datetime.now(timezone.utc)
        report.updated_at = datetime.now(timezone.utc)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Жалоба отклонена',
            'report': report.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/reports/<int:report_id>/actions', methods=['POST'])
@jwt_required()
@admin_required(level=4)
def take_action(report_id):
    """Выполнить действие над контентом (удаление, скрытие и т.д.)"""
    try:
        data = request.get_json()
        action = data.get('action')
        report = Report.query.get_or_404(report_id)
        
        current_user_id = get_jwt_identity()
        
        # Проверяем, что жалоба назначена текущему пользователю
        if report.assigned_admin_id != current_user_id:
            return jsonify({'error': 'Вы не назначены на эту жалобу'}), 403
        
        target_info = report.get_target_info()
        
        # Выполняем действие в зависимости от типа цели
        if report.target_type == 'post':
            post = Post.query.get(report.target_id)
            if post:
                if action == 'delete':
                    db.session.delete(post)
                elif action == 'hide':
                    post.status = 'hidden'
                elif action == 'warn_author':
                    # Можно добавить логику предупреждения автора
                    pass
                    
        elif report.target_type == 'comment':
            comment = Comment.query.get(report.target_id)
            if comment:
                if action == 'delete':
                    db.session.delete(comment)
                elif action == 'hide':
                    comment.status = 'hidden'
                    
        elif report.target_type == 'product':
            product = Product.query.get(report.target_id)
            if product:
                if action == 'delete':
                    db.session.delete(product)
                elif action == 'hide':
                    product.status = 'hidden'
                elif action == 'deactivate':
                    product.is_active = False
                    
        elif report.target_type == 'manual':
            manual = MaintenanceManual.query.get(report.target_id)
            if manual:
                if action == 'delete':
                    db.session.delete(manual)
                elif action == 'hide':
                    manual.status = 'hidden'
                elif action == 'unpublish':
                    manual.status = 'draft'
        
        db.session.commit()
        
        return jsonify({
            'message': f'Действие "{action}" выполнено успешно',
            'target_info': target_info
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/reports/stats', methods=['GET'])
@jwt_required()
@admin_required(level=4)
def get_reports_stats():
    """Получить статистику по жалобам"""
    try:
        # Общая статистика
        total_reports = Report.query.count()
        pending_reports = Report.query.filter_by(status='pending').count()
        reviewing_reports = Report.query.filter_by(status='reviewing').count()
        
        # Статистика по типам
        by_type = {
            'post': Report.query.filter_by(target_type='post').count(),
            'comment': Report.query.filter_by(target_type='comment').count(),
            'product': Report.query.filter_by(target_type='product').count(),
            'manual': Report.query.filter_by(target_type='manual').count(),
        }
        
        # Статистика по приоритетам
        by_priority = {
            'high': Report.query.filter_by(priority='high').count(),
            'medium': Report.query.filter_by(priority='medium').count(),
            'low': Report.query.filter_by(priority='low').count(),
        }
        
        # Статистика по статусам
        by_status = {
            'pending': pending_reports,
            'reviewing': reviewing_reports,
            'resolved': Report.query.filter_by(status='resolved').count(),
            'dismissed': Report.query.filter_by(status='dismissed').count(),
        }
        
        return jsonify({
            'stats': {
                'total': total_reports,
                'pending': pending_reports,
                'reviewing': reviewing_reports,
                'by_type': by_type,
                'by_priority': by_priority,
                'by_status': by_status
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
