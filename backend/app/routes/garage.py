from flask import Blueprint, request, jsonify
from app import db
from app.models import Motorcycle, MotorcycleMaintenance, MotorcycleNote, Member
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date, timedelta

garage = Blueprint('garage', __name__)

@garage.route('/api/garage/motorcycle/<int:moto_id>', methods=['GET'])
@jwt_required()
def get_motorcycle_detail(moto_id):
    current_user_id = get_jwt_identity()

    moto = Motorcycle.query.filter_by(id=moto_id, user_id=current_user_id).first()

    if not moto:
        return jsonify({ 'error': 'Motorcycle not found' }), 404
    
    maintenance_tasks = MotorcycleMaintenance.query.filter_by(
        motorcycle_id=moto_id
    ).order_by(MotorcycleMaintenance.next_maintenance_date).all()

    notes = MotorcycleNote.query.filter_by(
        motorcycle_id=moto_id
    ).order_by(MotorcycleNote.is_pinned.desc(), MotorcycleNote.updated_at.desc()).all()

    stats = moto.get_maintenance_stats()

    upcoming_tasks = [task for task in maintenance_tasks
                      if task.status == 'pending'][:3]
    
    return jsonify({
        'motorcycle': moto.to_dict(),
        'maintenance_tasks': [task.to_dict() for task in maintenance_tasks if task.status == 'pending'],
        'notes': [note.to_dict() for note in notes],
        'stats': stats,
        'all_tasks': [task.to_dict() for task in maintenance_tasks if task.status != 'completed'],
        'upcoming_maintenance': [task.to_dict() for task in upcoming_tasks],
        'recent_notes': [note.to_dict() for note in notes[:5]]
    })

@garage.route('/api/motorcycle/<int:moto_id>/mileage', methods=['PUT'])
@jwt_required()
def update_mileage(moto_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()

    moto = Motorcycle.query.filter_by(id=moto_id, user_id=current_user_id).first()

    if not moto:
        return jsonify({ 'error': 'Motorcycle not found' }), 404
    
    try:
        new_mileage = int(data.get('mileage', 0))
        if new_mileage < 0:
            return jsonify({ 'error': 'Mileage must be positive' }), 400
        
        old_mileage = moto.current_mileage
        moto.current_mileage = new_mileage
        
        tasks = MotorcycleMaintenance.query.filter_by(
            motorcycle_id=moto_id,
            schedule_type='mileage',
            status='pending'
        ).all()

        updated_tasks = []
        for task in tasks:
            if new_mileage >= task.next_maintenance_mileage:
                task.status = 'overdue'
                updated_tasks.append(task)

        db.session.commit()

        return jsonify({
            'motorcycle': moto.to_dict(),
            'updated_tasks': len(updated_tasks),
            'message': f'Mileage updated from {old_mileage} to {new_mileage}'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({ 'error': f'Error updating mileage: {str(e)}' }), 500
    
@garage.route('/api/garage/maintenance', methods=['POST'])
@jwt_required()
def add_maintenance():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    moto_id = data.get('motorcycle_id')
    moto = Motorcycle.query.filter_by(id=moto_id, user_id=current_user_id).first()
    
    if not moto:
        return jsonify({ 'error': 'Motorcycle not found' }), 404
    
    try:
        next_date = None
        next_mileage = None
        last_maintenance_date = None

        last_date_str = data.get('last_maintenance_date')
        if last_date_str:
            try:
                last_maintenance_date = datetime.fromisoformat(last_date_str.replace('Z', '+00:00')).date()
            except ValueError:
                last_maintenance_date = datetime.strptime(last_date_str, '%Y-%m-%d').date()
        else:
            last_maintenance_date = date.today()
        
        if data.get('schedule_type') == 'mileage':
            interval = data.get('interval_value', 0)
            last_mileage = data.get('last_maintenance_mileage', moto.current_mileage)
            next_mileage = last_mileage + interval
        elif data.get('schedule_type') == 'time':
            interval = data.get('interval_value', 0)
            unit = data.get('interval_unit', 'months')
            
            if unit == 'months':
                next_date = last_maintenance_date + timedelta(days=interval * 30)
            elif unit == 'days':
                next_date = last_maintenance_date + timedelta(days=interval)
        
        new_task = MotorcycleMaintenance(
            motorcycle_id=moto_id,
            title=data.get('title'),
            description=data.get('description'),
            maintenance_type=data.get('maintenance_type', 'regular'),
            schedule_type=data.get('schedule_type'),
            interval_value=data.get('interval_value'),
            interval_unit=data.get('interval_unit'),
            last_maintenance_date=last_maintenance_date,
            last_maintenance_mileage=data.get('last_maintenance_mileage'),
            next_maintenance_date=next_date,
            next_maintenance_mileage=next_mileage,
            priority=data.get('priority', 'medium'),
            cost=float(int(data.get('cost', 0))) if data.get('cost') else 0.0,
            parts_used=data.get('parts_used', ''),
            is_recurring=data.get('is_recurring', True),
            notes=data.get('notes'),
            status=data.get('status') if data.get('status') else 'pending'
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({
            'task': new_task.to_dict(),
            'message': 'Maintenance task created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({ 'error': f'Error creating maintenance task: {str(e)}' }), 500
    
@garage.route('/api/garage/maintenance/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_maintenance(task_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()

    task = MotorcycleMaintenance.query.get(task_id)
    if not task:
        return jsonify({ 'error': 'Task not found' }), 404
    
    moto = Motorcycle.query.filter_by(
        id=task.motorcycle_id,
        user_id=current_user_id
    ).first()

    if not moto:
        return jsonify({ 'error': 'Access denied' }), 403
    
    try:
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
            if data['status'] == 'completed':
                task.completed_at = datetime.now()
        if 'cost' in data:
            task.cost = data['cost']
        if 'parts_used' in data:
            task.parts_used = data['parts_used']
        if 'notes' in data:
            task.notes = data['notes']
        if 'priority' in data:
            task.priority = data['priority']

        db.session.commit()

        return jsonify({
            'task': task.to_dict(),
            'message': 'Task updated successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({ 'error': f'Error updating task: {str(e)}'}), 500
    
@garage.route('/api/garage/maintenance/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_maintenance(task_id):
    current_user_id = get_jwt_identity()

    task = MotorcycleMaintenance.query.get(task_id)
    if not task:
        return jsonify({ 'error': 'Task not found' }), 404
    
    moto = Motorcycle.query.filter_by(
        id=task.motorcycle_id,
        user_id=current_user_id
    ).first()

    if not moto:
        return jsonify({ 'error': 'Access denied' }), 403
    
    try:
        db.session.delete(task)
        db.session.commit()

        return jsonify({ 'error': 'Task deleted successfully' }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({ 'error': f'Error deleting task: {str(e)}'}), 500
    
@garage.route('/api/garage/maintenance/<int:task_id>/complete', methods=['POST'])
@jwt_required()
def complete_maintenance(task_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()

    task = MotorcycleMaintenance.query.get(task_id)
    if not task:
        return jsonify({ 'error': 'Task not found' }), 404
    
    moto = Motorcycle.query.filter_by(
        id=task.motorcycle.id,
        user_id=current_user_id
    ).first()
    if not moto:
        return jsonify({ 'error': 'Access denied' }), 403
    
    try:
        task.status = 'completed'
        task.completed_at = datetime.now()

        if 'cost' in data:
            task.cost = data['cost']
        if 'part_user' in data:
            print(data['parts_used'])
            task.parts_used = data['parts_used']    
        if 'notes' in data:
            task.notes = data['notes']

        if task.is_recurring:
            new_task = MotorcycleMaintenance(
                motorcycle_id=task.motorcycle_id,
                title=task.title,
                description=task.description,
                maintenance_type=task.maintenance_type,
                schedule_type=task.schedule_type,
                interval_value=task.interval_value,
                interval_unit=task.interval_unit,
                last_maintenance_date=datetime.now().date(),
                last_maintenance_mileage=moto.current_mileage,
                priority=task.priority,
                is_recurring=True,
                notes=task.notes,
                status='pending'
            )

            if task.schedule_type == 'mileage':
                new_task.next_maintenance_mileage = moto.current_mileage + task.interval_value
            elif task.schedule_type == 'time':
                if task.interval_value == 'months':
                    next_date = datetime.now().date() + timedelta(days=task.interval_value * 30)
                else:
                    next_date = datetime.now().date + timedelta(days=task.interval_value)
                new_task.next_maintenance_date = next_date

            db.session.commit()

            return jsonify({
                'task': task.to_dict(),
                'message': 'Task marked as completed'
            }), 200
    
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({ 'error': f'Error completing task: {str(e)}' }), 500

@garage.route('/api/garage/motorcycle/<int:moto_id>/history', methods=['GET'])
@jwt_required()
def get_maintenance_history(moto_id):
    current_user_id = get_jwt_identity()

    moto = Motorcycle.query.filter_by(
        id=moto_id,
        user_id=current_user_id
    ).first()
    if not moto:
        return jsonify({ 'error': 'Motorcycle not found' }), 404
    
    completed_tasks = MotorcycleMaintenance.query.filter_by(
        motorcycle_id=moto_id,
        status='completed'
    ).order_by(MotorcycleMaintenance.completed_at.desc()).all()

    return jsonify({
        'history': [task.to_dict() for task in completed_tasks],
        'total': len(completed_tasks)
    })

@garage.route('/api/garage/notes', methods=['POST'])
@jwt_required()
def add_note():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    moto_id = data.get('motorcycle_id')
    moto = Motorcycle.query.filter_by(id=moto_id, user_id=current_user_id).first()

    if not moto:
        return jsonify({ 'error': 'Motorcycle not found' }), 404
    
    try:
        new_note = MotorcycleNote(
            motorcycle_id=moto_id,
            title=data.get('title'),
            content=data.get('content'),
            category=data.get('category', 'general'),
            tags=data.get('tags', []),
            is_pinned=data.get('is_pinned', False)
        )
        
        db.session.add(new_note)
        db.session.commit()
        
        return jsonify({
            'note': new_note.to_dict(),
            'message': 'Note created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({ 'error': f'Error creating note: {str(e)}' }), 500
    
@garage.route('/api/garage/motorcycle/<int:moto_id>/notes', methods=['GET'])
@jwt_required()
def get_notes(moto_id):
    current_user_id = get_jwt_identity()

    moto = Motorcycle.query.filter_by(id=moto_id, user_id=current_user_id).first()
    if not moto:
        return jsonify({ 'error': 'Motorcycle not found' }), 404
    
    notes = MotorcycleNote.query.filter_by(
        motorcycle_id=moto_id
    ).order_by(
        MotorcycleNote.is_pinned.desc(),
        MotorcycleNote.updated_at.desc()
    ).all()

    return jsonify({
        'notes': [note.to_dict() for note in notes],
        'total': len(notes)
    })

@garage.route('/api/garage/notes/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()

    note = MotorcycleNote.query.get(note_id)
    if not note:
        return jsonify({ 'error': 'Note not found' }), 404
    
    moto = Motorcycle.query.filter_by(
        id=note.motorcycle_id,
        user_id=current_user_id
    ).first()

    if not moto: 
        return jsonify({ 'error': 'Access denied' }), 403
    
    try:
        if 'title' in data:
            note.title = data['title']
        if 'content' in data:
            note.content = data['content']
        if 'category' in data:
            note.category = data['category']
        if 'tags' in data:
            note.tags = data['tags']
        if 'is_pinned' in data:
            note.is_pinned = data['is_pinned']
        
        db.session.commit()
        
        return jsonify({
            'note': note.to_dict(),
            'message': 'Note updated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({ 'error': f'Error updating note: {str(e)}' }), 500
    
@garage.route('/api/garage/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    current_user_id = get_jwt_identity()

    note = MotorcycleNote.query.get(note_id)
    if not note:
        return jsonify({ 'error': 'Note not found' }), 404
    
    moto = Motorcycle.query.filter_by(
        id=note.motorcycle_id,
        user_id=current_user_id
    ).first()

    if not moto:
        return jsonify({ 'error': 'Access denied' }), 403
    
    try:
        db.session.delete(note)
        db.session.commit()

        return jsonify({ 'message': 'Note deleted successfully' }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({ 'error': f'Error deleting notes: {str(e)}'}), 500
    
@garage.route('/api/garage/overview', methods=['GET'])
@jwt_required()
def garage_overview():
    current_user_id = get_jwt_identity()

    motorcycles = Motorcycle.query.filter_by(user_id=current_user_id).all()

    total_maintenance_tasks = 0
    overdue_tasks = 0
    upcoming_tasks = []

    for moto in motorcycles:
        tasks = MotorcycleMaintenance.query.filter_by(
            motorcycle_id=moto.id
        ).all()

        total_maintenance_tasks += len(tasks)
        overdue_tasks += len([t for t in tasks if t.check_overdue()])

        for task in tasks:
            if task.status == 'pending' and task.next_maintenance_date:
                days_until = (task.next_maintenance_date - date.today()).days
                if 0 <= days_until <= 7:
                    task_dict = task.to_dict()
                    task_dict['motorcycle'] = {
                        'id': moto.id,
                        'brand': moto.brand,
                        'model': moto.model,
                        'license_plate': moto.license_plate
                    }
                    task_dict['days_until'] = days_until
                    upcoming_tasks.append(task_dict)
    
    upcoming_tasks.sort(key=lambda x: x.get('next_maintenance_date', ''))
    
    return jsonify({
        'total_motorcycles': len(motorcycles),
        'total_maintenance_tasks': total_maintenance_tasks,
        'overdue_tasks': overdue_tasks,
        'upcoming_tasks': upcoming_tasks[:5],  # Ближайшие 5 задач
        'motorcycles': [moto.to_dict() for moto in motorcycles]
    })