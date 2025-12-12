from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Member, Course, UserCoursesHistory

courses = Blueprint('courses', __name__)

@courses.route('/api/courses/get', methods=['GET'])
@jwt_required()
def get_courses():
    current_user_id = get_jwt_identity()
    user = Member.query.get(current_user_id)
    if not user:
        return jsonify({ 'error': 'User not found' }), 404
    
    all_courses = Course.get.all()
    all_courses_data = [{
        'id': c.id,
        'title': c.title,
        'description': c.description,
        'level': c.level,
        'ico': c.ico,
        'lessons': len(c.lessons),
    } for c in all_courses]

    # TODO: [] - Добавить курсы пользователя