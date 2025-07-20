import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.models import db, Device, FindEvent
from sqlalchemy.orm.session import close_all_sessions

# Load database URLs
sqlite_url = os.environ.get('SQLITE_DATABASE_URI', 'sqlite:///instance/echotag.db')
postgres_url = os.environ.get('SQLALCHEMY_DATABASE_URI')

if not postgres_url:
    raise EnvironmentError("Environment variable SQLALCHEMY_DATABASE_URI is not set.")

print(f"📦 Migrating data from:\nSQLite → {sqlite_url}\nPostgreSQL → {postgres_url}")

# Create SQLAlchemy engines
sqlite_engine = create_engine(sqlite_url)
postgres_engine = create_engine(postgres_url)

# Create tables in Postgres using model metadata
print("🛠️ Creating tables in PostgreSQL...")
db.metadata.create_all(bind=postgres_engine)

# Setup sessions
SqliteSession = sessionmaker(bind=sqlite_engine)
PostgresSession = sessionmaker(bind=postgres_engine)
sqlite_session = SqliteSession()
postgres_session = PostgresSession()

try:
    # --- Migrate Devices ---
    print("🔄 Migrating Devices...")
    devices = sqlite_session.query(Device).all()
    for device in devices:
        postgres_session.merge(Device(
            tool_id=device.tool_id,
            name=device.name
        ))

    # --- Migrate FindEvents ---
    print("🔄 Migrating FindEvents...")
    find_events = sqlite_session.query(FindEvent).all()
    for event in find_events:
        postgres_session.merge(FindEvent(
            tool_id=event.tool_id,
            timestamp=event.timestamp,
            message=event.message,
            finder_id=event.finder_id,
            location=event.location,
            image_url=event.image_url,
            image_filename=event.image_filename,
            thread_id=event.thread_id,
            reconnect_id=event.reconnect_id,
            notified=event.notified
        ))

    postgres_session.commit()
    print("✅ Migration complete.")

except Exception as e:
    postgres_session.rollback()
    print("❌ Error during migration:", e)

finally:
    sqlite_session.close()
    postgres_session.close()
    close_all_sessions()
