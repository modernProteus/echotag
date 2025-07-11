# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

class Config:
	# Base directory for building paths
	BASE_DIR = os.path.abspath(os.path.dirname(__file__))

	# SQLAlchemy config
	SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'echotag.db')}"
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Image display mode: 'local' or 'hosted'
	IMAGE_MODE = "local"  # can switch to "hosted" for production

	# Image path options
	LOCAL_IMAGE_PATH = "/static/images/"
	HOSTED_IMAGE_PATH = "https://cdn.j-scan.me/images/"

	# Discord webhook (static for now, can make dynamic later)
	DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

	# Optional credentials (currently unused but defined for extensibility)
	DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
	DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
	GMAIL_USER = os.getenv("GMAIL_USER")
	GMAIL_PASS = os.getenv("GMAIL_PASS")
