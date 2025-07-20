# backend/db/init_postgres.py

from backend.db.models import db
from backend.app import app

with app.app_context():
    db.create_all()
    print("✅ Tables created in PostgreSQL.")
