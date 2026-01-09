from . import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class Member(db.Model):
    __tablename__ = 'members'  

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='member')  
    join_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    is_verified = db.Column(db.Boolean, default=False)
    verification_date = db.Column(db.DateTime, nullable=True)

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
    
    member = db.relationship('Member', backref=db.backref('motorcycles', lazy=True))

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

    likes = db.relationship(
        'Like',
        primaryjoin="and_(Like.target_type=='product', foreign(Like.target_id)==Product.id)",
        viewonly=True
    )

class Post(db.Model):
    __tablename__ = 'posts'  

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)
    html_content = db.Column(db.Text, nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)  
    author = db.relationship('Member', backref='posts', lazy=True)  

    view_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) 
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))  

class Comment(db.Model):
    __tablename__ = 'comments'  

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  
    author_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)  
    
    author = db.relationship('Member', backref='comments', lazy=True)  
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))  

    like_count = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))  

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