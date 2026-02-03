from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Report, Post, Comment, Product, MaintenanceManual

user_reports = Blueprint('user_reports', __name__)

@user_reports.route('/reports', methods=['POST'])
@jwt_required()
def create_report():
    """ Create report to content """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        if str(data.get('target_owner_id')) == str(current_user_id):
            return jsonify({'error': 'Нельзя жаловаться на собственный контент'}), 400
        
        existing_report = Report.query.filter_by(
            reporter_id=current_user_id,
            target_id=data.get('target_id'),
            target_type=data.get('target_type')
        ).first()

        if existing_report:
            return jsonify({'error': 'Вы уже отправляли жалобу на этот контент'}), 400
        
        report = Report(
            reporter_id=current_user_id,
            target_id=data.get('target_id'),
            target_type=data.get('target_type'),
            reported_user_id=data.get('target_owner_id'),
            reason=data.get('reason'),
            details=data.get('details', ''),
            priority=data.get('priority', 'low'),
            status='pending'
        )

        db.session.add(report)
        db.session.commit()

        return jsonify({
            'message': 'Жалоба отправлена',
            'report': report.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@user_reports.route('/reports/check', methods=['GET'])
@jwt_required()
def check_user_report():
    """ Check existing user report """
    try:
        current_user_id = get_jwt_identity()
        target_id = request.args.get('target_id')
        target_type = request.args.get('target_type')

        report = Report.query.filter_by(
            reporter_id=current_user_id,
            target_id=target_id,
            target_type=target_type
        ).first()

        return jsonify({
            'has_reported': report is not None
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@user_reports.route('/reports/count', methods=['GET'])
def get_report_count():
    """ Get report count on content """
    try:
        target_id = request.args.get('target_id')
        target_type = request.args.get('target_type')

        count = Report.query.filter_by(
            target_id=target_id,
            target_type=target_type
        ).count()

        return jsonify({
            'count': count
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_reports.route('/reports/user', methods=['GET'])
@jwt_required()
def get_user_reports():
    """Получить список жалоб текущего пользователя"""
    try:
        current_user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        reports = Report.query.filter_by(reporter_id=current_user_id)\
            .order_by(Report.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        reports_data = []
        for report in reports.items:
            reports_data.append(report.to_dict())
        
        return jsonify({
            'reports': reports_data,
            'total': reports.total,
            'pages': reports.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        print(f"Error getting user reports: {e}")
        return jsonify({'error': str(e)}), 500


def check_target_exists(target_type, target_id):
    """Проверить существование целевого контента"""
    try:
        if target_type == 'post':
            target = Post.query.get(target_id)
        elif target_type == 'comment':
            target = Comment.query.get(target_id)
        elif target_type == 'product':
            target = Product.query.get(target_id)
        elif target_type == 'manual':
            target = MaintenanceManual.query.get(target_id)
        else:
            return False
        
        return target is not None
    except Exception as e:
        print(f"Error checking target exists: {e}")
        return False