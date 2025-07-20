# backend/db/init_postgres.py

from backend.app import app
from backend.db.models import db

with app.app_context():
    print(f"📡 Using DB: {app.config['SQLALCHEMY_DATABASE_URI']}")
    db.create_all()
    print("✅ Tables created in PostgreSQL.")
