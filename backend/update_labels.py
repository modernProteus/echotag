from backend.db.models import db, Device
from backend.app import app

# ID-to-name updates
updates = {
    "JC105": "Manfrotto - Mini Friction Arm",
    "JC106": "Manfrotto - MEGA Clamp",
    "JC107": "Manfrotto - Mini Friction Arm",
    "JC108": "Manfrotto - Micro Clamp",
    "JC109": "Manfrotto - Mini Friction Arm",
    "JC110": "Manfrotto - Micro Clamp",
}

with app.app_context():
    updated = 0

    for tool_id, new_name in updates.items():
        device = db.session.get(Device, tool_id)

        if device:
            print(f"🔎 {tool_id} — BEFORE: {device.name}")
            device.name = new_name
            print(f"✅ {tool_id} — UPDATED TO: {device.name}")
            updated += 1
        else:
            print(f"❌ {tool_id} — Not found")

    db.session.commit()
    print(f"\n🔁 Done. {updated} device(s) updated.\n")
