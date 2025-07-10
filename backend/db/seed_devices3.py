from backend.app import create_app
from backend.db.models import db, Device

app = create_app()

new_devices = [
	("JC123", "HD - DigiCo"),
	("JC124", "HD - Yamaha"),
	("JC125", "HD - PI"),
	("JC126", "HD - A&H"),
	("JC127", "HD - AVID"),
	("JC128", "HD - REC1"),
	("JC129", "HD - REC2"),
]

with app.app_context():
	for tool_id, name in new_devices:
		if not Device.query.get(tool_id):
			device = Device(
				id=tool_id,
				name=name,
				image_filename=f"{tool_id}.jpg",  # You can adjust or remove this if not needed
				image_url=f"/static/images/{tool_id}.jpg",
				notes=""
			)
			db.session.add(device)
			print(f"✅ Added {tool_id} – {name}")
		else:
			print(f"⚠️ Skipped {tool_id} – already exists")
	db.session.commit()
	print("🔁 Done seeding HD devices.")