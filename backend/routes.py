from flask import Blueprint, request, jsonify, render_template
from db.models import Device
from config import Config

DISCORD_CHANNEL_ID = Config.DISCORD_CHANNEL_ID
DISCORD_BOT_TOKEN = Config.DISCORD_BOT_TOKEN
GMAIL_USER = Config.GMAIL_USER
GMAIL_PASS = Config.GMAIL_PASS

from datetime import datetime
import uuid
import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

routes_blueprint = Blueprint("routes", __name__)
DISCORD_API_URL = "https://discord.com/api/v10"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"

def reverse_geocode(location):
	try:
		lat, lon = map(str.strip, location.split(","))
		res = requests.get(NOMINATIM_URL, params={
			'lat': lat,
			'lon': lon,
			'format': 'json'
		}, headers={'User-Agent': 'EchoTagApp'})
		if res.status_code == 200:
			data = res.json()
			address = data.get('address', {})
			return f"{address.get('city', '')}, {address.get('state', '')}".strip(', ')
	except Exception as e:
		print(f"Reverse geocode failed: {e}")
	return None

def send_email_html(tool_id, finder_id, auth_mode, message, location, image_url, thread_id):
	auth_status = 'Authenticated' if auth_mode == 'auth' else 'Anonymous'
	html_body = render_template(
		'echotag_email.html',
		tool_id=tool_id,
		finder_id=finder_id,
		auth_status=auth_status,
		location=location,
		message=message,
		image_url=image_url,
		thread_id=thread_id,
		discord_channel_id=DISCORD_CHANNEL_ID
	)

	msg = MIMEMultipart('alternative')
	msg['Subject'] = f"🔔 EchoTag Report – {tool_id}"
	msg['From'] = GMAIL_USER
	msg['To'] = "Jeremy@j-scan.me"
	part_html = MIMEText(html_body, 'html')
	msg.attach(part_html)

	try:
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
			server.login(GMAIL_USER, GMAIL_PASS)
			server.sendmail(GMAIL_USER, msg['To'], msg.as_string())
	except Exception as e:
		print(f"Email send failed: {e}")

@routes_blueprint.route('/api/report', methods=['POST'])
def report_tool():
	try:
		tool_id = request.form.get('tool_id', 'UNKNOWN').strip().upper()
		message = request.form.get('message', '').strip()
		finder_id = request.form.get('finderId', 'Anonymous')
		auth_mode = request.form.get('authMode', 'anon')
		location = request.form.get('location', None)
		image = request.files.get('image')

		# Lookup device
		device = Device.query.filter_by(id=tool_id).first()
		device_name = device.name if device else "Unknown"
		device_image_url = f"https://cdn.j-scan.me/images/{tool_id}.jpg"  # Can switch to local logic if needed

		# Localize time to CST
		cst_time = datetime.utcnow().strftime("%I:%M %p CST")

		short_id = uuid.uuid4().hex[:6]
		thread_name = f"{tool_id} – {device_name} – {cst_time} – {short_id}"

		headers = {
			"Authorization": f"Bot {DISCORD_BOT_TOKEN}",
			"Content-Type": "application/json"
		}

		# Create thread
		thread_payload = {
			"name": thread_name,
			"type": 11,
			"auto_archive_duration": 1440
		}

		thread_res = requests.post(
			f"{DISCORD_API_URL}/channels/{DISCORD_CHANNEL_ID}/threads",
			json=thread_payload,
			headers=headers
		)
		thread_res.raise_for_status()
		thread_id = thread_res.json()["id"]

		# Prepare message
		location_text = None
		if location:
			location_text = reverse_geocode(location) or location
			location_link = f"https://maps.google.com/?q={location}"
		else:
			location_link = None

		content_lines = [
			f"📦 **Tool ID:** `{tool_id}`",
			f"🔖 **Name:** {device_name}",
			f"🆔 **Finder:** `{finder_id}` ({'Authenticated' if auth_mode == 'auth' else 'Anonymous'})",
			f"📝 **Message:** {message or '_No message provided_'}"
		]

		if location_text:
			content_lines.append(f"📍 **Location:** [{location_text}]({location_link})")

		if device_image_url:
			content_lines.append(f"📷 **Device:** [Image]({device_image_url})")

		# Send main post
		requests.post(
			f"{DISCORD_API_URL}/channels/{thread_id}/messages",
			json={"content": "\n".join(content_lines)},
			headers=headers
		)

		# Send uploaded image as file, if any
		if image:
			upload_url = f"{DISCORD_API_URL}/channels/{thread_id}/messages"
			file_payload = {
				"file": (image.filename, image.stream, image.mimetype)
			}
			requests.post(upload_url, headers={"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}, files=file_payload)

		# Send email
		send_email_html(tool_id, finder_id, auth_mode, message, location_text, device_image_url, thread_id)

		return jsonify({
			"status": "ok",
			"thread_id": thread_id,
			"reconnect_url": f"https://j-scan.me/respond?thread={thread_id}"
		})

	except Exception as e:
		print(f"Report error: {e}")
		return jsonify({"error": str(e)}), 500

@routes_blueprint.route("/api/device", methods=["GET"])
def get_device():
	tool_id = request.args.get("id", "").strip().upper()
	if not tool_id:
		return jsonify({"error": "Missing device ID"}), 400

	device = Device.query.filter_by(id=tool_id).first()
	if not device:
		return jsonify({"error": "Device not found"}), 404

	return jsonify({
		"id": device.id,
		"name": device.name,
		"image_url": device.image_url,
		"notes": device.notes
	})

@routes_blueprint.route("/found")
def found_page():
	return render_template("found.html")
