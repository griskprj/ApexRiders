# migration_script.py
from app import create_app
from app.models import MotorcycleMaintenance, db

app = create_app()

with app.app_context():
    all_maintenance = MotorcycleMaintenance.query.filter_by(motorcycle_id=1)
    for t in all_maintenance:
        db.session.delete(t)

    db.session.commit()