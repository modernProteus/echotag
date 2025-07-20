from flask import Flask
from backend.db.models import db
from backend.routes import main as main_routes
from backend.routes import api as api_routes

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get(
    "SQLALCHEMY_DATABASE_URI", 
    "sqlite:///backend/instance/echotag.db"
)

db.init_app(app)

# Register routes
app.register_blueprint(main_routes)
app.register_blueprint(api_routes)

if __name__ == "__main__":
    app.run(debug=True)
