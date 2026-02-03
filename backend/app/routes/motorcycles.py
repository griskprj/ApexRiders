from flask import Blueprint, request, jsonify
from app import db
from app.models import Member, Motorcycle
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

motorcycle = Blueprint('motorcycle', __name__)


@motorcycle.route('/api/motorcycle', methods=['POST'])
@jwt_required()
def add_moto():
    """ Add motorcycle """
    data = request.get_json()
    current_user_id = get_jwt_identity()

    if not data.get('brand') or not data.get('model'):
        return jsonify({'error': 'Brand and model are required'}), 400

    try:
        insurance_expiry_str = data.get('insurance_expiry')
        insurance_expiry = None
        if insurance_expiry_str:
            try:
                insurance_expiry = datetime.fromisoformat(
                    insurance_expiry_str.replace('Z', '+00:00')).date()
            except ValueError:
                insurance_expiry = datetime.strptime(
                    insurance_expiry_str, '%Y-%m-%d').date()

        new_moto = Motorcycle(
            brand=data.get('brand'),
            model=data.get('model'),
            year=data.get('year'),
            engine_volume=data.get('engine_volume'),
            color=data.get('color'),
            license_plate=data.get('license_plate'),
            vin=data.get('vin'),
            insurance_expiry=insurance_expiry,
            user_id=current_user_id
        )

        db.session.add(new_moto)
        db.session.commit()

        return jsonify({
            'motorcycle': {
                'id': new_moto.id,
                'brand': new_moto.brand,
                'model': new_moto.model,
                'year': new_moto.year,
                'engine_volume': new_moto.engine_volume,
                'color': new_moto.color,
                'license_plate': new_moto.license_plate
            },
            'message': 'Motorcycle create successfully'
        })
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': f'Errro in create moto: {str(e)}'}), 500


@motorcycle.route('/api/motorcycle', methods=['GET'])
@jwt_required()
def my_motos():
    """ User motorcycles """
    current_user_id = get_jwt_identity()
    user = Member.query.get(current_user_id)

    motorcycles = Motorcycle.query.filter_by(user_id=user.id).all()

    moto_data = ([{
        'id': moto.id,
        'brand': moto.brand,
        'model': moto.model,
        'year': moto.year,
        'engine_volume': moto.engine_volume,
        'color': moto.color,
        'license_plate': moto.license_plate,
        'vin': moto.vin,
        'insurance_expiry': moto.insurance_expiry
    } for moto in motorcycles])

    return jsonify(moto_data)


@motorcycle.route('/api/motorcycle/<int:moto_id>', methods=['PUT'])
@jwt_required()
def update_moto(moto_id):
    """ Update motorcycle """
    data = request.get_json()
    current_user_id = get_jwt_identity()

    moto = Motorcycle.query.filter_by(
        id=moto_id, user_id=current_user_id).first()

    if not moto:
        return jsonify({'error': 'Motorcycle not found'}), 404

    insurance_expiry_str = data.get('insurance_expiry', moto.insurance_expiry)
    try:
        insurance_expiry = datetime.fromisoformat(
            insurance_expiry_str.replace('Z', '+00.00')).date()
    except ValueError:
        insurance_expiry = datetime.strptime(
            insurance_expiry_str, '%Y-%m-%d').date()

    try:
        moto.brand = data.get('brand', moto.brand)
        moto.model = data.get('model', moto.model)
        moto.year = data.get('year', moto.year)
        moto.engine_volume = data.get('engine_volume', moto.engine_volume)
        moto.color = data.get('color', moto.color)
        moto.license_plate = data.get('license_plate', moto.license_plate)
        moto.vin = data.get('vin', moto.vin)
        moto.insurance_expiry = insurance_expiry

        db.session.commit()

        return jsonify({
            'id': moto.id,
            'brand': moto.brand,
            'model': moto.model,
            'year': moto.year,
            'engine_volume': moto.engine_volume,
            'color': moto.color,
            'license_plate': moto.license_plate
        }), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': f'Error updating motorcycle: {str(e)}'}), 500


@motorcycle.route('/api/motorcycle/<int:moto_id>', methods=['DELETE'])
@jwt_required()
def delete_moto(moto_id):
    """ Delete motorcycle """
    current_user_id = get_jwt_identity()

    moto = Motorcycle.query.filter_by(
        id=moto_id, user_id=current_user_id).first()

    if not moto:
        return jsonify({'error': 'Motorcycle not found'}), 404

    try:
        db.session.delete(moto)
        db.session.commit()

        return jsonify({'error': 'Motorcycle delete successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting motorcycle: {str(e)}'}), 500
