# backend/db/init_postgres.py

from backend.db.models import db
from backend.app import app

print(f"📡 Using DB: {app.config['SQLALCHEMY_DATABASE_URI']}")

with app.app_context():
    db.create_all()
    print("✅ Tables created in PostgreSQL.")
