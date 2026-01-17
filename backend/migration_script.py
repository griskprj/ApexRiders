# migration_script.py
from app import create_app
from app.models import MotorcycleMaintenance, db

app = create_app()

with app.app_context():
    t1 = MotorcycleMaintenance.query.get(4)
    db.session.delete(t1)

    db.session.commit()