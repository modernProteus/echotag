# backend/db/init_postgres.py

import os
from backend.db.models import db, Device, FindEvent  # <-- Explicit model import
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI',
    'sqlite:///instance/echotag.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    print(f"📡 Using DB: {app.config['SQLALCHEMY_DATABASE_URI']}")
    db.init_app(app)
    db.create_all()
    print("✅ Tables created in PostgreSQL.")
