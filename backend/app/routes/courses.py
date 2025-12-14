from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Member, Course, Lesson, UserCoursesHistory, UserLessonHistory

courses = Blueprint('courses', __name__)

@courses.route('/api/courses/get', methods=['GET'])
@jwt_required()
def get_courses():
    current_user_id = get_jwt_identity()
    user = Member.query.get(current_user_id)
    if not user:
        return jsonify({ 'error': 'User not found' }), 404
    
    try :
        all_courses = Course.query.all()
        all_courses_data = [{
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'level': c.level,
            'ico': c.ico,
            'lessons': len(c.lessons),
        } for c in all_courses]

        user_courses = UserCoursesHistory.query.all()
        user_courses_data = [{
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'level': c.level,
            'ico': c.ico,
            'lessons': Lesson.query.filter_by(course_id=c.id).count(),
            'progress': UserLessonHistory.query.filter_by(course_id=c.id) / Lesson.query.filter_by(course_id=c.id)
        } for c in user_courses]

        return jsonify({
            'all_courses': all_courses_data,
            'user_courses': user_courses_data
        })
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({ 'error': f'Ошибка при получении курсов: {e}'}), 500