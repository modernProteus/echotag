import os
from backend.app import create_app
from backend.db.models import db, Device

import qrcode
import qrcode.image.svg  # SVG support
from io import BytesIO

# Folder to output SVGs
OUTPUT_DIR = "qr"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Base URL for each QR code
BASE_URL = "https://j-scan.me/found?id="

def generate_svg_qr(tool_id):
	url = f"{BASE_URL}{tool_id}"

	factory = qrcode.image.svg.SvgImage  # Or use SvgPathImage, SvgFragmentImage
	qr = qrcode.QRCode(
		version=4,
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=10,
		border=4,
	)
	qr.add_data(url)
	qr.make(fit=True)

	img = qr.make_image(image_factory=factory)

	output_path = os.path.join(OUTPUT_DIR, f"{tool_id}.svg")
	with open(output_path, "wb") as f:
		img.save(f)
	print(f"✅ Saved {tool_id}.svg")

def generate_all_qr_from_db():
	app = create_app()
	with app.app_context():
		tools = Device.query.all()
		for device in tools:
			generate_svg_qr(device.id)

if __name__ == "__main__":
	generate_all_qr_from_db()