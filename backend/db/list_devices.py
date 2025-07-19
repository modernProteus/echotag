from backend.db.models import db, Device
from backend.app import app

with app.app_context():
	devices = Device.query.order_by(Device.id).all()

	print(f"{'Tool ID':<8} | Name")
	print("-" * 40)

	for device in devices:
		print(f"{device.id:<8} | {device.name}")
	
	print(f"\nTotal: {len(devices)} tools")
