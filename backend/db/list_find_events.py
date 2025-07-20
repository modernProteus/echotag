# backend/db/list_find_events.py

from backend.db.models import db, FindEvent
from backend.app import app

with app.app_context():
    events = FindEvent.query.order_by(FindEvent.timestamp.desc()).all()

    if not events:
        print("⚠️  No find events found.")
    else:
        print("Tool ID  | Thread ID           | Timestamp           | Message")
        print("-" * 80)
        for event in events:
            print(f"{event.tool_id:<8} | {event.thread_id:<20} | {event.timestamp} | {event.message or '—'}")
        
        print(f"\nTotal: {len(events)} find events")
