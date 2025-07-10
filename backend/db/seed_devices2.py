from backend.app import create_app
from backend.db.models import db, Device

app = create_app()

tools_to_add = [
	("JC100", "Spectrum Analyzer"),
	("JC101", "Vector Network Analyzer"),
	("JC102", "MacBook"),
	("JC103", "Sound Bullet"),
	("JC104", "Q-Box"),
	("JC105", "ManFrodo - Mega Clamp"),
	("JC106", "Mega-Clamp"),
	("JC107", "ManFrodo - Mini Clamp 1"),
	("JC108", "Mini Clamp 1"),
	("JC109", "ManFrodo - Mini Clamp 2"),
	("JC110", "Mini Clamp 2"),
	("JC111", "Mic - SM58s"),
	("JC112", "Mic - SE-PTT"),
	("JC113", "Mic - SYS TUNE"),
	("JC114", "iPad Air"),
	("JC115", "Antenna - Sure UA860SWB"),
	("JC116", "PTouch Printer"),
	("JC117", "Focusrite - Scarlett 2i2"),
	("JC118", "5-Port Switch"),
	("JC119", "In-Ears - A6t"),
	("JC120", "In-Ears - A4t"),
	("JC121", "Rat Sniffer - Male"),
	("JC122", "Rat Sniffer - Female"),
]

with app.app_context():
	for tool_id, name in tools_to_add:
		existing = Device.query.get(tool_id)
		if not existing:
			new_tool = Device(
				id=tool_id,
				name=name,
				image_url=f"/static/images/{tool_id}.jpg",
				image_filename=f"{tool_id}.jpg",
				notes=""
			)
			db.session.add(new_tool)
			print(f"Added: {tool_id} – {name}")
		else:
			print(f"Skipped (already exists): {tool_id}")
	db.session.commit()
	print("✅ Device seeding complete (local image paths).")