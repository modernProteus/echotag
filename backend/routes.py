from flask import Blueprint, request, render_template, jsonify
from backend.db.models import db, Device, FindEvent

# === Page Routes ===
main = Blueprint("main", __name__)

@main.route("/respond")
def respond():
    thread_id = request.args.get("thread")
    if not thread_id:
        return "Missing thread ID", 400
    return render_template("response.html", thread=thread_id)

# === API Routes ===
api = Blueprint("api", __name__)

@api.route("/api/device")
def get_device():
    tool_id = request.args.get("id")
    if not tool_id:
        return jsonify({"error": "Missing tool ID"}), 400

    device = Device.query.get(tool_id)
    if not device:
        return jsonify({"error": "Device not found"}), 404

    return jsonify({
        "id": device.id,
        "name": device.name,
        "image_url": device.image_url,
        "notes": device.notes,
    })

@api.route("/api/response")
def get_response():
    thread_id = request.args.get("thread")
    if not thread_id:
        return jsonify({"error": "Missing thread ID"}), 400

    event = FindEvent.query.filter_by(thread_id=thread_id).first()
    if not event:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "toolId": event.tool_id,
        "message": event.message
    })
