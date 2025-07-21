import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.models import Device

# ID-to-name updates
updates = {
    "JC105": "Manfrotto - Mini Friction Arm",
    "JC106": "Manfrotto - MEGA Clamp",
    "JC107": "Manfrotto - Mini Friction Arm",
    "JC108": "Manfrotto - Micro Clamp",
    "JC109": "Manfrotto - Mini Friction Arm",
    "JC110": "Manfrotto - Micro Clamp",
}

# Load PostgreSQL URI
DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
if not DATABASE_URI:
    raise EnvironmentError("SQLALCHEMY_DATABASE_URI environment variable not set.")

# Connect to PostgreSQL
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

print("🔄 Applying label updates to PostgreSQL...\n")

updated = 0
for device_id, new_name in updates.items():
    device = session.query(Device).filter_by(id=device_id).first()
    if device:
        old_name = device.name or "(none)"
        device.name = new_name
        updated += 1
        print(f"✅ {device_id}: '{old_name}' → '{new_name}'")
    else:
        print(f"⚠️ Device ID {device_id} not found.")

session.commit()
session.close()

print(f"\n🎉 Done. {updated} device(s) updated.")
