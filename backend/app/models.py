from . import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class Member(db.Model):
    __tablename__ = 'members'  

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512))
    role = db.Column(db.String(20), default='member')  
    join_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime)

    is_verified = db.Column(db.Boolean, default=False)
    verification_date = db.Column(db.DateTime, nullable=True)

    admin_level = db.Column(db.Integer, default=False)
    is_super_admin = db.Column(db.Boolean, default=False)
    last_admin_login = db.Column(db.DateTime, nullable=True)

    manual_progress = db.relationship('UserManualProgress', back_populates='user', lazy=True)
    manual_ratings = db.relationship('ManualRating', back_populates='user', lazy=True)

    manual_history = db.relationship(
        'UserManualHistory',
        back_populates='user'
    )

    lesson_history = db.relationship(
        'UserLessonHistory',
        back_populates='user'
    )

    courses_history = db.relationship(
        'UserCoursesHistory',
        back_populates='user'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Motorcycle(db.Model):
    __tablename__ = 'motorcycles'  
    
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    engine_volume = db.Column(db.Integer)
    color = db.Column(db.String(50))
    license_plate = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)  
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    current_mileage = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    vin = db.Column(db.String(50))
    insurance_expiry = db.Column(db.Date)
    registration_expiry = db.Column(db.Date)
    
    member = db.relationship('Member', backref=db.backref('motorcycles', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'engine_volume': self.engine_volume,
            'color': self.color,
            'license_plate': self.license_plate,
            'current_mileage': self.current_mileage,
            'image_url': self.image_url,
            'vin': self.vin,
            'insurance_expiry': self.insurance_expiry.isoformat() if self.insurance_expiry else None,
            'registration_expiry': self.registration_expiry.isoformat() if self.registration_expiry else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'maintenance_stats': self.get_maintenance_stats()
        }
    
    def get_maintenance_stats(self):
        tasks = self.maintenance_tasks
        completed = len([t for t in tasks if t.status == 'completed'])
        pending = len([t for t in tasks if t.status == 'pending'])
        overdue = len([t for t in tasks if t.check_overdue()])

        return {
            'total_tasks': len(tasks),
            'completed': completed,
            'pending': pending,
            'overdue': overdue,
            'completion_rate': round((completed / len(tasks) * 100) if tasks else 0)
        }

class MotorcycleNote(db.Model):
    __tablename__ = 'motorcycle_notes'

    id = db.Column(db.Integer, primary_key=True)
    motorcycle_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    category = db.Column(db.String(50)) # maintenance, repair, modification, general
    tags = db.Column(db.JSON, default=list)
    is_pinned = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    motorcycle = db.relationship('Motorcycle', backref=db.backref('notes', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'motorcycle_id': self.motorcycle_id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'tags': self.tags or [],
            'is_pinned': self.is_pinned,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Course(db.Model):
    __tablename__ = 'courses'  

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=False)
    level = db.Column(db.String(64), nullable=False)
    ico = db.Column(db.String(256), nullable=False)

    lessons = db.relationship('Lesson', backref='course', lazy=True, order_by='Lesson.order')

class UserCoursesHistory(db.Model):
    __tablename__ = 'user_courses_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)  
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_id', name='unique_user_course'),
    )

    user = db.relationship('Member', back_populates='courses_history')
    course = db.relationship('Course')

class Lesson(db.Model):
    __tablename__ = 'lessons'  

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)  
    order = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    content_blocks = db.relationship('LessonBlock', backref='lesson', lazy=True, order_by='LessonBlock.order')

class LessonBlock(db.Model):
    __tablename__ = 'lesson_blocks'  

    TYPE_TEXT = 'text'
    TYPE_IMAGE = 'image'
    TYPE_VIDEO = 'video'
    TYPE_QUOTE = 'quote'
    TYPE_HEADER = 'header'

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)  
    _type = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    meta = db.Column(db.JSON)

class UserLessonHistory(db.Model):
    __tablename__ = 'user_lesson_history'  
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)  
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  

    __table_args__ = (
        db.UniqueConstraint('user_id', 'lesson_id', name='unique_user_lesson'),
    )

    user = db.relationship('Member', back_populates='lesson_history')  
    lesson = db.relationship('Lesson')



class DjimhanScheme(db.Model):
    __tablename__ = 'djimhana_schemes'  

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)

class Product(db.Model):
    __tablename__ = 'products'  

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=False)
    images = db.Column(db.JSON)
    cost = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    town = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    date_pub = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  
    watchs = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    is_bargain = db.Column(db.Boolean, default=False)
    likes_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(45), default='active')

    owner_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)  
    owner = db.relationship('Member', backref='products', lazy=True)

class Post(db.Model):
    __tablename__ = 'posts'  

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)  
    
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)
    html_content = db.Column(db.Text, nullable=True)

    like_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    image_filename = db.Column(db.String(256), nullable=True, default=None)
    image_url = db.Column(db.String(500), nullable=True, default=None)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) 
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), 
                       onupdate=lambda: datetime.now(timezone.utc)) 
    
    author = db.relationship('Member', backref='posts', lazy=True)  
    comments = db.relationship('Comment', backref='post')

class Comment(db.Model):
    __tablename__ = 'comments'  

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  
    author_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)  
    
    author = db.relationship('Member', backref='comments', lazy=True)  

    like_count = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), 
                       onupdate=lambda: datetime.now(timezone.utc))

class Like(db.Model):
    __tablename__ = 'likes'  

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)  
    
    target_type = db.Column(db.String(20), nullable=False) # post, product
    target_id = db.Column(db.Integer, nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'target_type', 'target_id', name='unique_like'),
    )

class MotorcycleMaintenance(db.Model):
    __tablename__ = 'motorcycle_maintenance'

    id = db.Column(db.Integer, primary_key=True)
    motorcycle_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id'), nullable=False)

    title = db.Column(db.Text)
    description = db.Column(db.Text)
    maintenance_type = db.Column(db.String(50)) # regular, repair, custom

    schedule_type = db.Column(db.String(20)) # mileage, time, date
    interval_value = db.Column(db.Integer)
    interval_unit = db.Column(db.String(20)) # km, months, days
    last_maintenance_date = db.Column(db.Date)
    last_maintenance_mileage = db.Column(db.Integer)
    next_maintenance_date = db.Column(db.Date)
    next_maintenance_mileage = db.Column(db.Integer)

    status = db.Column(db.String(20), default='pending') # pending, completed, overdue
    is_recurring = db.Column(db.Boolean, default=True)
    priority = db.Column(db.String(20), default='medium') # low, medium, high

    cost = db.Column(db.Float)
    parts_used = db.Column(db.Text)
    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    motorcycle = db.relationship('Motorcycle', backref=db.backref('maintenance_tasks', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'motorcycle_id': self.motorcycle_id,
            'title': self.title,
            'description': self.description,
            'maintenance_type': self.maintenance_type,
            'schedule_type': self.schedule_type,
            'interval_value': self.interval_value,
            'interval_unit': self.interval_unit,
            'last_maintenance_date': self.last_maintenance_date if self.last_maintenance_date else None,
            'last_maintenance_mileage': self.last_maintenance_mileage,
            'next_maintenance_date': self.next_maintenance_date if self.next_maintenance_date else None,
            'next_maintenance_mileage': self.next_maintenance_mileage,
            'status': self.status,
            'is_recurring': self.is_recurring,
            'priority': self.priority,
            'cost': self.cost,
            'parts_used': self.parts_used or [],
            'notes': self.notes,
            'created_at': self.created_at if self.created_at else None,
            'completed_at': self.completed_at if self.completed_at else None,
            'status': self.status,
            'is_overdue': self.check_overdue()
        }
    
    def check_overdue(self):
        if self.status == 'completed':
            return False
        
        now = datetime.now(timezone.utc).date()
        
        if self.next_maintenance_date and self.next_maintenance_date < now:
            return True
        
        if (self.motorcycle and 
            self.next_maintenance_mileage and 
            self.motorcycle.current_mileage >= self.next_maintenance_mileage):
            return True
            
        return False

class MaintenanceManual(db.Model):
    __tablename__ = 'manuals'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    moto_type = db.Column(db.String(50))
    
    category = db.Column(db.String(50))
    difficulty = db.Column(db.String(20))
    estimated_time = db.Column(db.String(50))
    tools_required = db.Column(db.JSON, default=list)
    parts_required = db.Column(db.JSON, default=list)
    warnings = db.Column(db.Text)
    
    views = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0)
    rating_count = db.Column(db.Integer, default=0)
    completions = db.Column(db.Integer, default=0)
    
    status = db.Column(db.String(20), default='draft')
    is_featured = db.Column(db.Boolean, default=False)
    
    author_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    author = db.relationship('Member', backref=db.backref('authored_manuals', lazy=True), foreign_keys=[author_id])
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    published_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    steps = db.relationship('ManualStep', back_populates='manual', lazy=True, order_by='ManualStep.order', cascade='all, delete-orphan')
    ratings = db.relationship('ManualRating', back_populates='manual', lazy=True)
    progress_records = db.relationship('UserManualProgress', back_populates='manual', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'moto_type': self.moto_type,
            'category': self.category,
            'difficulty': self.difficulty,
            'estimated_time': self.estimated_time,
            'tools_required': self.tools_required or [],
            'parts_required': self.parts_required or [],
            'warnings': self.warnings,
            'views': self.views,
            'rating': self.rating,
            'rating_count': self.rating_count,
            'completions': self.completions,
            'status': self.status,
            'is_featured': self.is_featured,
            'author_id': self.author_id,
            'author_username': self.author.username if self.author else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'step_count': len(self.steps) if self.steps else 0
        }
    
class ManualDraft(db.Model):
    __tablename__ = 'manual_drafts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    
    manual_data = db.Column(db.JSON)
    steps_data = db.Column(db.JSON)
    uploaded_images = db.Column(db.JSON, default=list)
    
    last_modified = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = db.relationship('Member', backref='manual_drafts', lazy=True)

class ManualStep(db.Model):
    __tablename__ = 'manual_steps'
    
    id = db.Column(db.Integer, primary_key=True)
    manual_id = db.Column(db.Integer, db.ForeignKey('manuals.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    image_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))
    
    warnings = db.Column(db.Text)
    tips = db.Column(db.Text)
    estimated_time = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    manual = db.relationship('MaintenanceManual', back_populates='steps')
    
    def to_dict(self):
        return {
            'id': self.id,
            'manual_id': self.manual_id,
            'order': self.order,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'video_url': self.video_url,
            'warnings': self.warnings,
            'tips': self.tips,
            'estimated_time': self.estimated_time,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class UserManualProgress(db.Model):
    __tablename__ = 'user_manual_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    manual_id = db.Column(db.Integer, db.ForeignKey('manuals.id'), nullable=False)
    
    completed_steps = db.Column(db.JSON, default=list)
    
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_activity = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    total_time_spent = db.Column(db.Integer, default=0)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'manual_id', name='unique_user_manual_progress'),
    )
    
    user = db.relationship('Member', back_populates='manual_progress')
    manual = db.relationship('MaintenanceManual', back_populates='progress_records')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'manual_id': self.manual_id,
            'completed_steps': self.completed_steps or [],
            'is_completed': self.is_completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'total_time_spent': self.total_time_spent,
            'progress_percentage': self.get_progress_percentage()
        }
    
    def get_progress_percentage(self):
        if not self.manual or not self.manual.steps:
            return 0
        total_steps = len(self.manual.steps)
        completed = len(self.completed_steps) if self.completed_steps else 0
        return round((completed / total_steps) * 100) if total_steps > 0 else 0
    
class ManualRating(db.Model):
    __tablename__ = 'manual_ratings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    manual_id = db.Column(db.Integer, db.ForeignKey('manuals.id'), nullable=False)

    rating = db.Column(db.Integer, nullable=False)

    comment = db.Column(db.Text)

    was_helpful = db.Column(db.Boolean, default=True)

    actual_difficulty = db.Column(db.String(20))
    actual_time_spent = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'manual_id', name='unique_user_manual_rating'),
    )

    user = db.relationship('Member', back_populates='manual_ratings')
    manual = db.relationship('MaintenanceManual', back_populates='ratings')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'manual_id': self.manual_id,
            'rating': self.rating,
            'comment': self.comment,
            'was_helpful': self.was_helpful,
            'actual_difficulty': self.actual_difficulty,
            'actual_time_spent': self.actual_time_spent,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_username': self.user.username if self.user else None
        }

class UserManualHistory(db.Model):
    __tablename__ = 'user_manual_history'  
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)  
    manual_id = db.Column(db.Integer, db.ForeignKey('manuals.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  

    __table_args__ = (
        db.UniqueConstraint('user_id', 'manual_id', name='unique_user_manual'),
    )

    user = db.relationship('Member', back_populates='manual_history')  
    manual = db.relationship('MaintenanceManual')


class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    
    notification_type = db.Column(db.String(50), nullable=False)  # like_post, like_comment, like_product, admin_report, admin_broadcast
    
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)
    
    target_type = db.Column(db.String(50))  # post, comment, product, admin
    target_id = db.Column(db.Integer)
    
    metadata_ = db.Column(db.JSON, default=dict)
    
    is_read = db.Column(db.Boolean, default=False)
    is_archived = db.Column(db.Boolean, default=False)
    
    admin_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=True)
    priority = db.Column(db.String(20), default='normal')  # low, normal, high
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    read_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship('Member', backref=db.backref('notifications', lazy=True), foreign_keys=[user_id])
    admin = db.relationship('Member', foreign_keys=[admin_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'notification_type': self.notification_type,
            'title': self.title,
            'message': self.message,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'metadata': self.metadata_ or {},
            'is_read': self.is_read,
            'is_archived': self.is_archived,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'admin_info': {
                'id': self.admin.id if self.admin else None,
                'username': self.admin.username if self.admin else None
            } if self.admin else None,
            'ago_time': self.get_ago_time()
        }
    
    def get_ago_time(self):
        if not self.created_at:
            return "только что"
        
        now = datetime.now(timezone.utc)
        
        # Убедимся, что created_at тоже offset-aware
        if self.created_at.tzinfo is None:
            # Если created_at без временной зоны, добавим UTC
            created_at_aware = self.created_at.replace(tzinfo=timezone.utc)
        else:
            created_at_aware = self.created_at
        
        diff = now - created_at_aware
        
        if diff.days > 365:
            years = diff.days // 365
            return f"{years} год назад" if years == 1 else f"{years} лет назад"
        elif diff.days > 30:
            months = diff.days // 30
            return f"{months} месяц назад" if months == 1 else f"{months} месяцев назад"
        elif diff.days > 0:
            return f"{diff.days} день назад" if diff.days == 1 else f"{diff.days} дней назад"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} час назад" if hours == 1 else f"{hours} часов назад"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} минуту назад" if minutes == 1 else f"{minutes} минут назад"
        else:
            return "только что"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.now(timezone.utc)