# migration_script.py
from app import create_app
from app.models import MotorcycleMaintenance, db

app = create_app()

with app.app_context():
    t1 = MotorcycleMaintenance.query.get(1)
    t2 = MotorcycleMaintenance.query.get(2)
    db.session.delete(t1)
    db.session.delete(t2)

    db.session.commit()