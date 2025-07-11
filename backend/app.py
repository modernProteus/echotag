from flask import Flask
from flask_cors import CORS
from routes import routes_blueprint
from db.models import db
from config import Config  # ✅ Import the Config class
import os

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)  # ✅ Load config from the class
	CORS(app)  # Enable cross-origin requests

	# Ensure folders exist
	os.makedirs("static/uploads", exist_ok=True)

	db.init_app(app)
	app.register_blueprint(routes_blueprint)
	return app

if __name__ == "__main__":
	app = create_app()
	app.run(debug=True)
