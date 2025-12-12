from flask import Blueprint, request, jsonify
from app import db
from app.models import Member
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

auth = Blueprint('auth', __name__)

@auth.route('/api/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()

    member = Member.query.filter_by(email=data.get('email')).first()

    if member and check_password_hash(member.password_hash, data.get('password')):
        access_token = create_access_token(
            identity=str(member.id),
            expires_delta=timedelta(hours=24)
        )

        return jsonify({
            'access_token': access_token,
            'member': {
                'id': member.id,
                'username': member.username,
                'email': member.email
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@auth.route('/api/auth/register', methods=['POST'])
def register_user():
    data = request.get_json()

    if not all([data.get('username'), data.get('email'), data.get('password')]):
        return jsonify({'error': 'Do not enter all the necessary information'}), 400

    if Member.query.filter_by(username=data.get('username')).first():
        return jsonify({'error': 'This username is already in use.'}), 400

    if Member.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'This email is already in use.'}), 400
    
    try:
        user = Member(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password'))
        )
        
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'access_token': access_token
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error.'}), 500
    
@auth.route('/api/auth/user', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        print(f"JWT Identity: {current_user_id}")
        
        user = Member.query.get(current_user_id)
        
        if not user:
            print("User not found in database")
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    except Exception as e:
        return jsonify({'error': 'Unable to fetch user data'}), 401

@auth.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout_user():
    return jsonify({'message': 'Successfully logged out'}), 200