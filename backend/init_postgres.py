from backend.db.models import db
from backend.app import app

with app.app_context():
    db.create_all()
    print("✅ PostgreSQL schema initialized")
