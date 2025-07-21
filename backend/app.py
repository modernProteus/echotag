from flask import Flask
from flask_cors import CORS
from backend.routes import routes_blueprint
from backend.db.models import db
from backend.config import Config
import os

def create_app():
    app = Flask(__name__)

    # ✅ Apply base config
    app.config.from_object(Config)

    # ✅ Apply correct DB URI before db.init_app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///backend/instance/echotag.db'
    )

    # ✅ Print so logs confirm the config before DB binds
    print(f"📡 Using SQLAlchemy DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    CORS(app)
    os.makedirs("static/uploads", exist_ok=True)

    db.init_app(app)
    app.register_blueprint(routes_blueprint)

    return app

# 🔥 Entry point for Gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
