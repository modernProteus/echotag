from flask import Flask
from flask_cors import CORS
from backend.routes import routes_blueprint
from backend.db.models import db
from backend.config import Config
import os

def create_app():
    app = Flask(__name__)

    # ✅ Set config from object first
    app.config.from_object(Config)

    # ✅ Explicitly set SQLALCHEMY_DATABASE_URI using env var
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///backend/instance/echotag.db'
    )

    CORS(app)
    os.makedirs("static/uploads", exist_ok=True)

    print(f"📡 Using SQLAlchemy DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # ✅ Initialize DB after config is fully loaded
    db.init_app(app)
    app.register_blueprint(routes_blueprint)
    return app

# 🔥 This must exist for Gunicorn to see it
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
