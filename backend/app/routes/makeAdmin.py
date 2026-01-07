from app import db
from models import Member

id = 1
user = Member.query.get(id)
user.is_verified = True

db.session.commit()