import qrcode
from PIL import Image
import os

# Base URL (update this if you're using localhost or staging)
BASE_URL = "https://j-scan.me/found?id="

# Folder to save generated QR codes
OUTPUT_DIR = "qr"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_qr(tool_id, glyph_path=None):
	url = f"{BASE_URL}{tool_id}"

	# Generate QR Code
	qr = qrcode.QRCode(
		version=4,
		error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for glyph
		box_size=10,
		border=4,
	)
	qr.add_data(url)
	qr.make(fit=True)

	qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

	# Optional: Add glyph/logo
	if glyph_path and os.path.exists(glyph_path):
		glyph = Image.open(glyph_path)
		# Resize glyph based on QR size
		qr_width, qr_height = qr_img.size
		glyph_size = int(qr_width * 0.2)
		glyph = glyph.resize((glyph_size, glyph_size), Image.LANCZOS)

		# Paste glyph at center
		pos = ((qr_width - glyph_size) // 2, (qr_height - glyph_size) // 2)
		qr_img.paste(glyph, pos, glyph if glyph.mode == 'RGBA' else None)

	# Save image
	qr_img.save(os.path.join(OUTPUT_DIR, f"{tool_id}.png"))
	print(f"✅ QR code generated for {tool_id}")

# Example usage
if __name__ == "__main__":
	# Replace with your real glyph path or pass None
	glyph_path = "design/jscan-glyph.png"

	tool_ids = ["JC123", "JC124", "JC125", "JC126", "JC127", "JC128", "JC129"]
	for tid in tool_ids:
		generate_qr(tid, glyph_path)