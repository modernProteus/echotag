from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

def generate_uuid():
	return str(uuid.uuid4())

# -------------------------------
# DEVICE MODEL
# -------------------------------
class Device(db.Model):
	__tablename__ = 'devices'

	id = db.Column(db.String, primary_key=True)  # e.g., JC045
	name = db.Column(db.String, nullable=False)
	image_url = db.Column(db.String)
	image_filename = db.Column(db.String, nullable=True)
	notes = db.Column(db.Text)
	active = db.Column(db.Boolean, default=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

	# Relationship to find events
	find_events = db.relationship("FindEvent", backref="device", lazy=True)

	def __repr__(self):
		return f"<Device {self.id} - {self.name}>"

# -------------------------------
# FIND EVENT MODEL
# -------------------------------
class FindEvent(db.Model):
	__tablename__ = 'find_events'

	id = db.Column(db.String, primary_key=True, default=generate_uuid)
	tool_id = db.Column(db.String, db.ForeignKey('devices.id'), nullable=False)

	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	message = db.Column(db.Text)
	finder_id = db.Column(db.String)
	location = db.Column(db.String)
	image_url = db.Column(db.String)
	image_filename = db.Column(db.String, nullable=True)
	thread_id = db.Column(db.String)      # Discord thread reference
	reconnect_id = db.Column(db.String)   # Used for /respond?thread=...
	notified = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return f"<FindEvent {self.id} for Tool {self.tool_id}>"