from backend.db.models import db, Device
from backend.app import app

with app.app_context():
    devices = Device.query.order_by(Device.tool_id).all()

    print("\n=== Devices in Database ===")
    for d in devices:
        print(f"{d.tool_id:<8} | {d.label}")
    print(f"\nTotal: {len(devices)} devices\n")
