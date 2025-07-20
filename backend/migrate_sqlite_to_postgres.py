import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.db.models import db, Device, FindEvent

# Load DB URIs from environment
SQLITE_URI = os.getenv("SQLITE_DATABASE_URI", "sqlite:///backend/instance/echotag.db")
POSTGRES_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

print("📦 Migrating data from:")
print(f"SQLite → {SQLITE_URI}")
print(f"PostgreSQL → {POSTGRES_URI}")

# Create engines
sqlite_engine = create_engine(SQLITE_URI)
postgres_engine = create_engine(POSTGRES_URI)

# Create tables in Postgres if not exist
print("🛠️ Creating tables in PostgreSQL...")
Device.metadata.create_all(postgres_engine)
FindEvent.metadata.create_all(postgres_engine)

# Set up sessions
SqliteSession = sessionmaker(bind=sqlite_engine)
PostgresSession = sessionmaker(bind=postgres_engine)

sqlite_session = SqliteSession()
postgres_session = PostgresSession()

try:
    print("🔄 Migrating Devices...")
    results = sqlite_session.execute(text("""
        SELECT id, name, image_url, image_filename, notes, active, created_at FROM devices
    """))

    for row in results:
        device = Device(
            tool_id=row.id,
            name=row.name,
            image_url=row.image_url,
            image_filename=row.image_filename,
            notes=row.notes,
            active=row.active,
            created_at=row.created_at
        )
        postgres_session.add(device)

    print("🔄 Migrating Find Events...")
    results = sqlite_session.execute(text("""
        SELECT tool_id, timestamp, message, finder_id, location,
               image_url, image_filename, thread_id, reconnect_id, notified
        FROM find_events
    """))

    for row in results:
        event = FindEvent(
            tool_id=row.tool_id,
            timestamp=row.timestamp,
            message=row.message,
            finder_id=row.finder_id,
            location=row.location,
            image_url=row.image_url,
            image_filename=row.image_filename,
            thread_id=row.thread_id,
            reconnect_id=row.reconnect_id,
            notified=row.notified
        )
        postgres_session.add(event)

    postgres_session.commit()
    print("✅ Migration complete!")

except Exception as e:
    postgres_session.rollback()
    print(f"❌ Error during migration: {e}")

finally:
    sqlite_session.close()
    postgres_session.close()
