import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.db.models import Device, FindEvent, db

# Load database URIs from environment
sqlite_uri = os.getenv("SQLITE_DATABASE_URI", "sqlite:///backend/instance/echotag.db")
postgres_uri = os.getenv("SQLALCHEMY_DATABASE_URI")

print("📦 Migrating data from:")
print(f"SQLite → {sqlite_uri}")
print(f"PostgreSQL → {postgres_uri}")

# Setup SQLite (source)
sqlite_engine = create_engine(sqlite_uri)
SQLiteSession = sessionmaker(bind=sqlite_engine)
sqlite_session = SQLiteSession()

# Setup PostgreSQL (destination)
postgres_engine = create_engine(postgres_uri)
PostgresSession = sessionmaker(bind=postgres_engine)
postgres_session = PostgresSession()

# Ensure tables exist in PostgreSQL
print("🛠️ Creating tables in PostgreSQL...")
db.metadata.create_all(bind=postgres_engine)

try:
    # Migrate Devices
    print("🔄 Migrating Devices...")
    result = sqlite_session.execute(text("SELECT * FROM devices"))
    for row in result.mappings():
        device = Device(
            id=row['id'],
            name=row['name'],
            image_url=row['image_url'],
            image_filename=row['image_filename'],
            notes=row['notes'],
            active=row['active'],
            created_at=row['created_at']
        )
        postgres_session.merge(device)  # merge handles upserts
    postgres_session.commit()
    print("✅ Devices migrated.")

    # Migrate Find Events
    print("🔄 Migrating Find Events...")
    result = sqlite_session.execute(text("SELECT * FROM find_events"))
    for row in result.mappings():
        event = FindEvent(
            id=row['id'],
            tool_id=row['tool_id'],
            timestamp=row['timestamp'],
            message=row['message'],
            finder_id=row['finder_id'],
            location=row['location'],
            image_url=row['image_url'],
            image_filename=row['image_filename'],
            thread_id=row['thread_id'],
            reconnect_id=row['reconnect_id'],
            notified=row['notified']
        )
        postgres_session.merge(event)
    postgres_session.commit()
    print("✅ Find events migrated.")

except Exception as e:
    print(f"❌ Error during migration: {e}")
finally:
    sqlite_session.close()
    postgres_session.close()
