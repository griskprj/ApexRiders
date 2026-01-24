from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime, timezone
import json
from app import db
from app.models import Member, MaintenanceManual, UserManualHistory, ManualStep, UserManualProgress, ManualDraft, ManualRating

manuals = Blueprint('manuals', __name__)

UPLOAD_FOLDER = 'static/uploads/manuals'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_user_verification(user_id):
    user = Member.query.get(user_id)

    return user and user.is_verified

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
        'description': m.description,
        'moto_type': m.moto_type,
        'category': m.category,
        'difficulty': m.difficulty,
        'estimated_time': m.estimated_time,
        'tools_required': m.tools_required,
        'parts_required': m.parts_required,
        'warnings': m.warnings,
        'views': m.views,
        'rating': m.rating,     
        'created_at': m.created_at.isoformat() if m.created_at else None,
    } for m in all_manuals ]

    user_manuals_history = UserManualHistory.query.filter_by(user_id=current_user_id) \
        .order_by(UserManualHistory.viewed_at.desc()) \
        .limit(3) \
        .all()
    user_manuals = [MaintenanceManual.query.get(manual_record.id) for manual_record in user_manuals_history]

    user_manuals_data = [{
        'id': m.id,
        'title': m.title,
    } for m in user_manuals]
    
    return jsonify({
        'manuals_data': manuals_data,
        'user_manuals': user_manuals_data
    })

@manuals.route('/api/manuals/get/<int:manual_id>', methods=['GET'])
@jwt_required()
def get_one_manual(manual_id):
    current_user_id = get_jwt_identity()
    user = Member.query.get(current_user_id)
    if not user:
        print('User not found')
        return jsonify({ 'error': 'User not found' }), 404
    
    is_verified = True if user.is_verified else False
    print(is_verified)
    
    manual = MaintenanceManual.query.get(manual_id)
    manual_data = {
        'id': manual.id,
        'title': manual.title,
        'description': manual.description,
        'moto_type': manual.moto_type,
        'category': manual.category,
        'difficulty': manual.difficulty or 'Начинающий',
        'estimated_time': manual.estimated_time or '',
        'tools': manual.tools_required or [],
        'materials': manual.parts_required or [],
        'warnings': manual.warnings or '',
        'views': manual.views,
        'rating': manual.rating,     
        'created_at': manual.created_at.isoformat() if manual.created_at else None,
    }

    manual.views += 1

    steps = ManualStep.query.filter_by(manual_id=manual_id).all()
    steps_data = [{
        'id': s.id,
        'title': s.title,
        'description': s.description,
        'image_url': s.image_url,
        'video_url': s.video_url,
    } for s in steps]

    db.session.commit()

    return jsonify({
        'manual': manual_data,
        'steps': steps_data,
        'user_verified': is_verified
    })

@manuals.route('/api/manuals/constructor/create', methods=['POST'])
@jwt_required()
def create_manual():
    current_user_id = get_jwt_identity()

    user = Member.query.get(current_user_id)
    if user.admin_level < 1:
        return jsonify({ 'error': 'Только пользователи с уровнем админа 1 могут создать мануалы'}), 403
    
    data = request.get_json()

    required_fields = ['title', 'moto_type', 'category', 'difficulty', 'description', 'steps']
    for filed in required_fields:
        if filed not in data or not data[filed]:
            return jsonify({ 'eror': f'Поле {filed} обязательно'}), 400
        
    steps = data.get('steps', [])
    if not steps:
        return jsonify({ 'error': 'Добавьте хотя бы один шаг' }), 400
    
    manual = MaintenanceManual(
        title=data['title'],
        moto_type=data['moto_type'],
        category=data['category'],
        difficulty=data['difficulty'],
        description=data['description'],
        estimated_time=data.get('estimated_time', ''),
        tools_required=data.get('tools', []),
        parts_required=data.get('materials', []),
        warnings=data.get('warnings', ''),
        author_id=current_user_id,
        status='published',
        published_at=datetime.now(timezone.utc)
    )

    db.session.add(manual)
    db.session.flush()

    for i, step_data in enumerate(steps):
        step = ManualStep(
            manual_id=manual.id,
            title=step_data['title'],
            description=step_data['description'],
            image_url=step_data.get('image_url', ''),
            video_url=step_data.get('video_url', ''),
            warnings=step_data.get('warnings', ''),
            tips=step_data.get('tips', ''),
            estimated_time=step_data.get('estimated_time', ''),
            order=step_data.get('order', i)
        )
        db.session.add(step)

    db.session.commit()

    draft = ManualDraft.query.filter_by(user_id=current_user_id).first()
    if draft:
        db.session.delete(draft)
        db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Мануал успешно создан',
        'manual_id': manual.id
    }), 201

@manuals.route('/api/manuals/constructor/draft', methods=['POST', 'GET', 'DELETE'])
@jwt_required()
def manage_draft():
    current_user_id = get_jwt_identity()

    if request.method == 'POST':
        data = request.get_json()

        draft = ManualDraft.query.filter_by(user_id=current_user_id).first()

        if draft:
            draft.manual_data = data.get('manual', {})
            draft.steps_data = data.get('steps', [])
            draft.last_modified = datetime.now(timezone.utc)
        else:
            draft = ManualDraft(
                user_id=current_user_id,
                manual_data=data.get('manual', {}),
                steps_data=data.get('steps', []),
                uploaded_images=data.get('uploaded_images', [])
            )
            db.session.add(draft)
        
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Черновик сохранен',
            'last_modified': draft.last_modified.isoformat()
        })
    
    elif request.method == 'GET':
        draft = ManualDraft.query.filter_by(user_id=current_user_id).first()

        if draft:
            manual_data = draft.manual_data or {}

            if 'tools' not in manual_data:
                manual_data['tools'] = []
            if 'materials' not in manual_data:
                manual_data['materials'] = []
            if 'warnings' not in manual_data:
                manual_data['warnings'] = ''
            if 'estimated_time' not in manual_data:
                manual_data['estimated_time'] = ''

            return jsonify({
                'manual': manual_data,
                'steps': draft.steps_data,
                'uploaded_images': draft.uploaded_images,
                'last_modified': draft.last_modified.isoformat(),
                'created_at': draft.created_at.isoformat()
            })
        else:
             return jsonify({
                'manual': {
                    'title': '',
                    'moto_type': '',
                    'category': '',
                    'difficulty': '',
                    'description': '',
                    'estimated_time': '',
                    'tools': [],
                    'materials': [],
                    'warnings': ''
                },
                'steps': [],
                'uploaded_images': [],
                'last_modified': None,
                'created_at': None
            })
    
    elif request.method == 'DELETE':
        draft = ManualDraft.query.filter_by(user_id=current_user_id).first()

        if draft:
            for image_url in (draft.uploaded_images or []):
                try:
                    filename = image_url.split('/')[-1]
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'manuals', 'drafts', filename)
                    if os.path.exists(filepath):
                        os.remove(filepath)
                except:
                    pass
            
            db.session.delete(draft)
            db.session.commit()
        
        return jsonify({ 'success': True, 'message': 'Черновик удален' })
    
@manuals.route('/api/manuals/constructor/upload-image', methods=['POST'])
@jwt_required()
def upload_image():
    current_user_id = get_jwt_identity()

    if 'image' not in request.files:
        return jsonify({ 'error': 'Файл не найден' }), 404
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({ 'error': 'Файл не выбран' }), 400
    
    if not allowed_file(file.filename):
        return jsonify({ 'error': 'Недопустимый тип файла. Разрешены: PNG, JPG, JPEG, GIF, WEBP' }), 400
    
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)

    if file_length > 5 * 1024 * 1024:
        return jsonify({ 'error': 'Файл слишком большой. Максимальный размер: 5MB' }), 400
    
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"

    is_draft = request.form.get('is_draft', 'false').lower() == 'true'
    folder = 'drafts' if is_draft else 'published'

    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'manuals', folder)
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, unique_filename)
    file.save(filepath)

    image_url = f"/uploads/manuals/{folder}/{unique_filename}"

    if is_draft:
        draft = ManualDraft.query.filter_by(user_id=current_user_id).first()
        if draft:
            uploaded_images = draft.uploaded_images or []
            uploaded_images.append(image_url)
            draft.uploaded_images = uploaded_images
            db.session.commit()
    
    return jsonify({
        'success': True,
        'image_url': image_url,
        'filename': unique_filename
    })

@manuals.route('/api/manuals/constructor/<int:manual_id>/progress', methods=['GET', 'POST', 'DELETE'])
@jwt_required()
def manage_progress(manual_id):
    current_user_id = get_jwt_identity()

    manual = MaintenanceManual.query.get_or_404(manual_id)

    if request.method == 'GET':
        progress = UserManualProgress.query.filter_by(
            user_id=current_user_id,
            manual_id=manual_id
        ).first()

        if progress:
            return jsonify(progress.to_dict())
        else:
            return jsonify({
                'user_id': current_user_id,
                'manual_id': manual_id,
                'completed_steps': [],
                'is_completed': False,
                'progress_percentage': 0
            })
    
    elif request.method == 'POST':
        data = request.get_json()
        step_id = data.get('step_id')
        completed = data.get('completed', True)

        progress = UserManualProgress.query.filter_by(
            user_id=current_user_id,
            manual_id=manual_id
        ).first()

        if not progress:
            progress = UserManualProgress(
                user_id=current_user_id,
                manual_id=manual_id,
                started_at=datetime.now(timezone.utc)
            )
            db.session.add(progress)
            db.session.flush()
        

        
        step = ManualStep.query.filter_by(manual_id=manual_id, id=step_id).first()
        if not step:
            return jsonify({ 'error': 'Шаг не найден' }), 404
        
        completed_steps = list(progress.completed_steps or [])

        if completed:
            if step_id not in completed_steps:
                completed_steps.append(step_id)
        else:
            if step_id in completed_steps:
                completed_steps.remove(step_id)
        
        progress.completed_steps = completed_steps
        progress.last_activity = datetime.now(timezone.utc)

        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(progress, 'completed_steps')

        all_steps = ManualStep.query.filter_by(manual_id=manual_id).all()
        total_steps = len(all_steps)
        completed_count = len(completed_steps)

        if completed_count >= total_steps and total_steps > 0:
            progress.is_completed = True
            progress.completed_at = datetime.now(timezone.utc)
            manual.completions += 1

        else:
            progress.is_completed = False
            progress.completed_at = None
        
        db.session.commit()

        return jsonify(progress.to_dict())
    
    elif request.method == 'DELETE':
        progress = UserManualProgress.query.filter_by(
            user_id=current_user_id,
            manual_id=manual_id
        ).first()

        if progress:
            db.session.delete(progress)
            db.session.commit()

        return jsonify({ 'success': True, 'message': 'Прогресс сброшен'})
    
@manuals.route('/api/manuals/constructor/<int:manual_id>/rate', methods=['POST'])
@jwt_required()
def rate_manual(manual_id):
    current_user_id = get_jwt_identity()

    manual = MaintenanceManual.query.get_or_404(manual_id)
    data = request.get_json()

    rating_value = data.get('rating')
    if not rating_value or not 1 <= rating_value <= 5:
        return jsonify({ 'error': 'Оценка должна быть от 1 до 5' }), 400
    
    progress = UserManualProgress.query.filter_by(
        user_id=current_user_id,
        manual_id=manual_id,
        is_completed=True
    ).first()

    if not progress:
        return jsonify({ 'error': 'Вы можете оценить только выполненный мануал' }), 400
    
    existing_rating = ManualRating.query.filter_by(
        user_id=current_user_id,
        manual_id=manual_id
    ).first()

    if existing_rating:
        old_rating = existing_rating.rating
        existing_rating.rating = rating_value
        existing_rating.comment = data.get('comment', existing_rating.comment)
        existing_rating.was_helpful = data.get('was_helpful', existing_rating.was_helpful)
        existing_rating.actual_difficulty = data.get('actual_difficulty', existing_rating.actual_difficulty)
        existing_rating.actual_time_spent = data.get('actual_time_spent', existing_rating.actual_time_spent)
        existing_rating.updated_at = datetime.now(timezone.utc)
    else:
        rating = ManualRating(
            user_id=current_user_id,
            manual_id=manual_id,
            rating=rating_value,
            comment=data.get('comment'),
            was_helpful=data.get('was_helpful', True),
            actual_difficulty=data.get('actual_difficulty', ''),
            actual_time_spent=data.get('actual_time_spent', '')
        )
        db.session.add(rating)
        old_rating = None

    ratings = ManualRating.filter_by(manual_id=manual_id).all()
    if ratings:
        total = sum(r.rating for r in ratings)
        count = len(ratings)
        manual.rating = total / count
        manual.rating_count = count
    
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Оценка сохранена',
        'average_rating': manual.rating,
        'rating_count': manual.rating_count
    })

@manuals.route('/api/manuals/constructor/verify-access', methods=['GET'])
@jwt_required()
def verify_access():
    current_user_id = get_jwt_identity()

    user = Member.query.get(current_user_id)
    if not user:
        return jsonify({ 'error': 'Пользователь не найден' }), 404
    
    return jsonify({
        'admin_level': user.admin_level,
        'username': user.username,
        'role': user.role,
        'verification_date': user.verification_date.isoformat() if user.verification_date else None
    })

@manuals.route('/api/manuals/constructor/user-manuals', methods=['GET'])
@jwt_required()
def get_user_manuals():
    current_user_id = get_jwt_identity()

    created_manuals = MaintenanceManual.query.filter_by(
        author_id=current_user_id,
    ).order_by(MaintenanceManual.created_at.desc()).all()

    progress_manuals = UserManualProgress.query.filter_by(
        user_id=current_user_id,
    ).order_by(UserManualProgress.last_activity.desc()).all()

    return jsonify({
        'created': [manual.to_dict() for manual in created_manuals],
        'in_progress': [{
            'manual': record.manual.to_dict(),
            'progress': record.to_dict()
        } for record in progress_manuals if not record.is_completed],
        'completed': [{
            'manual': record.manual.to_dict(),
            'progress': record.to_dict()
        } for record in progress_manuals if record.is_completed]
    })

@manuals.route('/api/manuals/<int:manual_id>/complete-all', methods=['POST'])
@jwt_required()
def complete_all(manual_id):
    current_user_id = get_jwt_identity()

    manual = MaintenanceManual.query.get(manual_id)
    if not manual:
        return jsonify({ 'error': 'Мануал не найден' }), 404
    
    progress = UserManualProgress.query.filter_by(
        user_id=current_user_id,
        manual_id=manual_id
    ).first()
    if not progress:
        progress = UserManualProgress(
            user_id=current_user_id,
            manual_id=manual_id,
            started_at=datetime.now(timezone.utc)
        )
        db.session.add(progress)
    
    user_manual_history = UserManualHistory.query.filter_by(user_id=current_user_id, manual_id=manual_id).first()
    if not user_manual_history:
        user_manual_history = UserManualHistory(
            user_id=current_user_id,
            manual_id=manual_id,
            viewed_at=datetime.now(timezone.utc)
        )
        db.session.add(user_manual_history)
    else:
        user_manual_history.viewed_at = datetime.now(timezone.utc)

    steps = ManualStep.query.filter_by(manual_id=manual_id).all()
    
    step_ids = [step.id for step in steps]
    
    progress.completed_steps = step_ids
    progress.is_completed = True
    progress.completed_at = datetime.now(timezone.utc)
    progress.last_activity = datetime.now(timezone.utc)

    manual.completions += 1
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Все шаги отмечены как выполненные',
        'progress': progress.to_dict()
    })

@manuals.route('/api/manuals/constructor/<int:manual_id>/edit', methods=['GET', 'PUT'])
@jwt_required()
def edit_manual(manual_id):
    current_user_id = get_jwt_identity()

    user = Member.query.get(current_user_id)
    if not user or not user.is_verified:
        return jsonify({ 'error': 'Только верифицированные пользователи могут редактировать мануалы' }), 403
    
    manual = MaintenanceManual.query.get_or_404(manual_id)

    if int(manual.author_id) != int(current_user_id):
        return jsonify({ 'error': 'Вы можете редактировать только свои мануалы' }), 403
    
    if request.method == 'GET':
        manual_data = {
            'id': manual.id,
            'title': manual.title,
            'description': manual.description,
            'moto_type': manual.moto_type,
            'category': manual.category,
            'difficulty': manual.difficulty,
            'estimated_time': manual.estimated_time,
            'tools': manual.tools_required or [],
            'materials': manual.parts_required or [],
            'warnings': manual.warnings,
            'status': manual.status,
            'author_id': manual.author_id
        }

        steps = ManualStep.query.filter_by(manual_id=manual_id).order_by(ManualStep.order).all()
        steps_data = [{
            'id': s.id,
            'title': s.title,
            'description': s.description,
            'image_url': s.image_url,
            'video_url': s.video_url,
            'order': s.order,
            'warnings': s.warnings,
            'tips': s.tips,
            'estimated_time': s.estimated_time
        } for s in steps]

        return jsonify({
            'manual': manual_data,
            'steps': steps_data,
            'can_edit': True
        })
    
    elif request.method == 'PUT':
        data = request.get_json()

        manual.title = data.get('title', manual.title)
        manual.moto_type = data.get('moto_type', manual.moto_type)
        manual.category = data.get('category', manual.category)
        manual.difficulty = data.get('difficulty', manual.difficulty)
        manual.description = data.get('description', manual.description)
        manual.estimated_time = data.get('estimated_time', manual.estimated_time)
        manual.tools_required = data.get('tools', manual.tools_required)
        manual.parts_required = data.get('materials', manual.parts_required)
        manual.warnings = data.get('warnings', manual.warnings)
        manual.updated_at = datetime.now(timezone.utc)

        steps_data = data.get('steps', [])

        ManualStep.query.filter_by(manual_id=manual_id).delete()

        for i, step_data in enumerate(steps_data):
            step = ManualStep(
                manual_id=manual.id,
                title=step_data['title'],
                description=step_data['description'],
                image_url=step_data.get('image_url', ''),
                video_url=step_data.get('video_url', ''),
                warnings=step_data.get('warnings', ''),
                tips=step_data.get('tips', ''),
                estimated_time=step_data.get('estimated_time', ''),
                order=step_data.get('order', i)
            )
            db.session.add(step)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Мануал успешно обновлен',
            'manual_id': manual.id
        })
    
@manuals.route('/api/manuals/constructor/<int:manual_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_manual(manual_id):
    current_user_id = get_jwt_identity()

    user = Member.query.get(current_user_id)
    if not user or not user.is_verified:
        return jsonify({ 'error': 'Только верифицированные пользователи могут удалять мануалы' }), 403
    
    manual = MaintenanceManual.query.get_or_404(manual_id)

    if int(manual.author_id) != int(current_user_id):
        return jsonify({ 'error': 'Вы можете удалять только свои мануалы' }), 403
    
    try:
        UserManualProgress.query.filter_by(manual_id=manual_id).delete()
        UserManualHistory.query.filter_by(manual_id=manual_id).delete()
        ManualRating.query.filter_by(manual_id=manual_id).delete()

        ManualStep.query.filter_by(manual_id=manual_id).delete()

        db.session.delete(manual)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Мануал успешно удален'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({ 'error': f'Ошибка при удалении: {str(e)}' }), 500