from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.models import Member, MaintenanceManual, UserManualHistory

manuals = Blueprint('manuals', __name__)

@manuals.route('/api/manuals/get', methods=['GET'])
@jwt_required()
def get_manuals():
    current_user_id = get_jwt_identity()
    user = Member.query.get(current_user_id)
    if not user:
        print('User not found')
        return jsonify({ 'error': 'User not found' }), 404
    
    all_manuals = MaintenanceManual.query.all()
    manuals_data = [{
        'id': m.id,
        'title': m.title,
        'desctiption': m.description,
        'moto_type': m.moto_type,
        'drive_type': m.drive_type,
        'difficulty': m.difficulty,
        'estimated_time': m.estimated_time,
        'created_at': m.created_at.isoformat() if m.created_at else None,
        'views': m.views,
        'rating': m.rating,     
    } for m in all_manuals ]

    user_manuals_all = UserManualHistory.query.filter_by(user_id=current_user_id) \
        .order_by(UserManualHistory.viewed_at.desc()) \
        .limit(3) \
        .all()
    
    user_manuals = [{
        'id': m.id,
        'title': m.title,
        'viewed_at': m.viewed_at.isoformat()
    } for m in user_manuals_all]
    
    return jsonify({
        'manuals_data': manuals_data,
        'user_manuals': user_manuals
    })