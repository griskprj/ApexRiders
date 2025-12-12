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
    images = db.Column(db.JSON, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    town = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    date_pub = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  
    watchs = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    is_bargain = db.Column(db.Boolean, default=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)  
    owner = db.relationship('Member', backref='products', lazy=True)

class Post(db.Model):
    __tablename__ = 'posts'  

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)

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
    drive_type = db.Column(db.String(20))
    difficulty = db.Column(db.String(20))
    estimated_time = db.Column(db.Integer)
    tools_required = db.Column(db.Text)
    parts_required = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  
    views = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0)

class ManualStep(db.Model):
    __tablename__ = 'manual_steps'  

    id = db.Column(db.Integer, primary_key=True)
    manual_id = db.Column(db.Integer, db.ForeignKey('manuals.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary)
    warning = db.Column(db.Text)
    tips = db.Column(db.Text)

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

MaintenanceManual.steps = db.relationship(
    'ManualStep', 
    backref='manual', 
    lazy='dynamic', 
    cascade='all, delete-orphan',
    order_by='ManualStep.step_number'
)