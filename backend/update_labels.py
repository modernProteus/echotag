from backend.db.models import db, Device
from backend.app import app

updates = {
    "JC105": "Manfrotto - Mini Friction Arm",
    "JC106": "Manfrotto - MEGA Clamp",
    "JC107": "Manfrotto - Mini Friction Arm",
    "JC108": "Manfrotto - Micro Clamp",
    "JC109": "Manfrotto - Mini Friction Arm",
    "JC110": "Manfrotto - Micro Clamp",
}

with app.app_context():
    for tool_id, new_label in updates.items():
        device = Device.query.get(tool_id)
        if device:
            device.label = new_label
            print(f"✅ Updated {tool_id} to '{new_label}'")
        else:
            print(f"❌ Tool {tool_id} not found")
    db.session.commit()
    print("🔁 Done updating labels.")
