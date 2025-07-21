import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.models import Device, FindEvent, db as postgres_db

# Load URIs
sqlite_uri = os.environ.get("SQLITE_DATABASE_URI", "sqlite:///backend/instance/echotag.db")
postgres_uri = os.environ.get("SQLALCHEMY_DATABASE_URI")

print("📦 Migrating data from:")
print(f"SQLite → {sqlite_uri}")
print(f"PostgreSQL → {postgres_uri}")

# Connect to SQLite
sqlite_engine = create_engine(sqlite_uri)
SQLiteSession = sessionmaker(bind=sqlite_engine)
sqlite_session = SQLiteSession()

# Connect to PostgreSQL
postgres_engine = create_engine(postgres_uri)
PostgresSession = sessionmaker(bind=postgres_engine)
postgres_session = PostgresSession()

# Create tables in PostgreSQL
print("🛠️ Creating tables in PostgreSQL...")
postgres_db.metadata.create_all(postgres_engine)

try:
    # Migrate Devices
    print("🔄 Migrating Devices...")
    sqlite_devices = sqlite_session.execute("SELECT * FROM devices").fetchall()
    for row in sqlite_devices:
        device = Device(
            id=row["id"],
            name=row["name"],
            image_url=row["image_url"],
            image_filename=row["image_filename"],
            notes=row["notes"],
            active=row["active"],
            created_at=row["created_at"]
        )
        postgres_session.merge(device)

    # Migrate FindEvents
    print("🔄 Migrating Find Events...")
    sqlite_events = sqlite_session.execute("SELECT * FROM find_events").fetchall()
    for row in sqlite_events:
        event = FindEvent(
            id=row["id"],
            tool_id=row["tool_id"],
            timestamp=row["timestamp"],
            message=row["message"],
            finder_id=row["finder_id"],
            location=row["location"],
            image_url=row["image_url"],
            image_filename=row["image_filename"],
            thread_id=row["thread_id"],
            reconnect_id=row["reconnect_id"],
            notified=row["notified"]
        )
        postgres_session.merge(event)

    postgres_session.commit()
    print(f"✅ Migrated {len(sqlite_devices)} devices and {len(sqlite_events)} find events.")

except Exception as e:
    print(f"❌ Error during migration: {e}")
    postgres_session.rollback()

finally:
    sqlite_session.close()
    postgres_session.close()
