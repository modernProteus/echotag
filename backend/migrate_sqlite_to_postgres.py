import os
from sqlalchemy import create_engine, MetaData, Table
from backend.db.models import db, Device, FindEvent
from backend.app import app

# -- Local SQLite DB path
SQLITE_PATH = "backend/instance/echotag.db"
SQLITE_URI = f"sqlite:///{SQLITE_PATH}"

# -- PostgreSQL target is already configured in your app
POSTGRES_URI = app.config["SQLALCHEMY_DATABASE_URI"]

def migrate_data():
    print(f"🔁 Connecting to SQLite: {SQLITE_PATH}")
    sqlite_engine = create_engine(SQLITE_URI)
    sqlite_conn = sqlite_engine.connect()
    sqlite_metadata = MetaData()
    sqlite_metadata.reflect(bind=sqlite_engine)

    # Reflect tables
    sqlite_devices = Table("devices", sqlite_metadata, autoload_with=sqlite_engine)
    sqlite_finds = Table("find_events", sqlite_metadata, autoload_with=sqlite_engine)

    # Fetch all rows
    device_rows = sqlite_conn.execute(sqlite_devices.select()).fetchall()
    find_rows = sqlite_conn.execute(sqlite_finds.select()).fetchall()

    with app.app_context():
        for row in device_rows:
            if not db.session.get(Device, row.id):
                device = Device(
                    id=row.id,
                    name=row.name,
                    image_url=row.image_url,
                    image_filename=row.image_filename,
                    notes=row.notes,
                    active=row.active,
                    created_at=row.created_at,
                )
                db.session.add(device)

        for row in find_rows:
            if not db.session.get(FindEvent, row.id):
                event = FindEvent(
                    id=row.id,
                    tool_id=row.tool_id,
                    timestamp=row.timestamp,
                    message=row.message,
                    finder_id=row.finder_id,
                    location=row.location,
                    image_url=row.image_url,
                    image_filename=row.image_filename,
                    thread_id=row.thread_id,
                    reconnect_id=row.reconnect_id,
                    notified=row.notified,
                )
                db.session.add(event)

        db.session.commit()
        print(f"✅ Migrated {len(device_rows)} devices and {len(find_rows)} find events.")

if __name__ == "__main__":
    migrate_data()
