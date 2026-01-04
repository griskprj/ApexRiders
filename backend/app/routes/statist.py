from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.models import Member, UserManualHistory, UserLessonHistory, Post, Product, Comment, UserCoursesHistory, Lesson

statistic = Blueprint('statistic', __name__)

""" Стата дашборд """
@statistic.route('/api/statistic/dashboard', methods=['GET'])
@jwt_required()
def dashboard_stat():
    current_user_id = get_jwt_identity()
    user = Member.query.get(current_user_id)

    if not user:
        return jsonify({ 'errror': 'User not found' }), 404

    # Стата уроков, мануалов и объявлений    
    manuals_count = UserManualHistory.query.filter_by(user_id=current_user_id).count()
    lessons_count = UserLessonHistory.query.filter_by(user_id=current_user_id).count()
    
    active_products = Product.query.filter_by(
        owner_id=current_user_id,
        is_active=True
    ).all()
    products_active_data = [{
        'id': p.id,
        'title': p.title,
        'cost': p.cost,
        'watchs': p.watchs,
        'likes_count': p.likes_count
    } for p in active_products]

    posts_count = Post.query.filter_by(author_id=current_user_id).count()

    # Стата лайков и комментов польз-я
    from sqlalchemy import func

    total_likes = db.session.query(func.sum(Post.like_count)) \
        .filter(Post.author_id == current_user_id) \
        .scalar() or 0
    
    answer_count = Comment.query.filter_by(author_id=current_user_id).count()

    # Стата просмотренных пользователем курсов и кол-во уроков, просмотренных в этом курсе
    user_courses = UserCoursesHistory.query.filter_by(user_id=current_user_id).all()

    courses_data = []
    for uc in user_courses:
        course = uc.course
        
        end_lessons = UserLessonHistory.query\
            .filter_by(user_id=current_user_id)\
            .join(Lesson)\
            .filter(Lesson.course_id == course.id)\
            .count()
        
        all_lessons = Lesson.query.filter_by(course_id=course.id).count()
        
        courses_data.append({
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'end_lessons': end_lessons,
            'all_lessons': all_lessons
        })

    return jsonify({
        'manuals_count': manuals_count,
        'lessons_count': lessons_count,
        'product_active_count': len(active_products),
        'active_product_data': products_active_data,
        'posts_count': posts_count,
        'total_likes': total_likes,
        'answer_count': answer_count,
        'courses': courses_data
    })