# backend/discord_notify.py

import requests
from datetime import datetime
from backend.config import Config

def send_discord_notification(tool_id, tool_name, image_url=None, message=None):
	#webhook_url = Config.DISCORD_WEBHOOK_URL
	app.config.from_object(Config)  # ✅ Load config from the class

	timestamp = datetime.utcnow().isoformat()
	content = f"📦 **Device Found** – `{tool_id}`\n**Name**: {tool_name}"
	if message:
		content += f"\n📝 Message: {message}"

	embed = {
		"title": f"Tool ID: {tool_id}",
		"description": tool_name,
		"timestamp": timestamp,
		"color": 0x00FFAA,
	}

	if image_url:
		embed["image"] = {"url": image_url}

	payload = {
		"content": content,
		"embeds": [embed],
	}

	try:
		response = requests.post(webhook_url, json=payload)
		response.raise_for_status()
		print(f"✅ Sent notification to Discord for {tool_id}")
	except Exception as e:
		print(f"❌ Failed to send Discord notification: {e}")