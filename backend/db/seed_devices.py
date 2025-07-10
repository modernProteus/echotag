from backend.app import create_app
from backend.db.models import db, Device

app = create_app()

with app.app_context():
	devices = Device.query.all()

	for device in devices:
		# Only update if it doesn't already include '/images/'
		if "/images/" not in device.image_url:
			# Strip domain or leading slash if present
			filename = device.image_url.split("/")[-1]
			device.image_url = f"/static/images/{filename}"
			print(f"Updated {device.id} → {device.image_url}")

	db.session.commit()
	print("✅ All image URLs updated.")