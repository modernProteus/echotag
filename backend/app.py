from flask import Flask
from flask_cors import CORS
from backend.routes import routes_blueprint
from backend.db.models import db
from backend.config import Config
import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///instance/echotag.db')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Ensure folders exist
    os.makedirs("static/uploads", exist_ok=True)

    db.init_app(app)
    app.register_blueprint(routes_blueprint)
    return app

# 🔥 This must exist for Gunicorn to see it
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
