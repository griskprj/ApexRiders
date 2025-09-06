from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

""" PENDING USER REGISTRATION """
class PendingRegistration(db.Model):
    __tablename__ = 'pending_registrations'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False), index=True
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(256), nullable=False, index=True)
    verification_token = db.Column(db.String(32), nullable=False)
    token_expiration = db.Column(db.DateTime, nullable=False)

    __tabel_args__ = {
        db.Index('ix_token_expiration', 'token_expiration')
    }

""" USER """
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(256), nullable=False, index=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.LargeBinary)

    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    motorcycles = db.relationship("Motorcycle", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

    def get_motorcycles_count(self):
        return len(self.motorcycles)
    
    def has_motorcycles(self):
        return bool(self.motorcycles)

""" MOTORCYCLE """
class Motorcycle(db.Model):
    __tablename__ = 'motorcycles'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), ondelete='CASCADE', nullable=False)
    model = db.Column(db.String(120), nullable=False)
    years_create = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    moto_type = db.Column(db.String(50), nullable=False)
    engine_volume = db.Column(db.Integer, nullable=False)
    drive_type = db.Column(db.String(20), nullable=False, default="chain")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.LargeBinary)

    owner = db.relationship("User", back_populates="motorcycles")

    __table_args__ = (
        db.Index('ix_owner_id', 'owner_id'),
        db.Index('ix_moto_type', 'moto_type'),
        db.Index('ix_engine_volume', 'engine_volume'),
    )

    def __repr__(self):
        return f'<Motorcycle {self.model} ({self.years_create})>'
