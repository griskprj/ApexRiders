from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Member, DjimhanScheme


djimhana = Blueprint('djimhana', __name__)

@djimhana.route('/schemes', methods=['GET'])
@jwt_required()
def get_schemes():
    """ Get schemes """
    try:
        schemes = DjimhanScheme.query.all()

        schemes_data = [{
            'id': s.id,
            'title': s.title,
            'description': s.decsription,
            'image': s.image
        } for s in schemes]

        return jsonify({
            'schemes': schemes_data
        })
    
    except Exception as e:
        current_app.logger.error(f'Error getting schemes: {str(e)}')
