# backend/migrate_sqlite_to_postgres.py

import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.db.models import db, Device, FindEvent

Base = declarative_base()

# ✅ Inline definition of the old SQLite schema
class LegacyDevice(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    tool_id = Column(String, unique=True, nullable=False)
    name = Column(String)

class LegacyFindEvent(Base):
    __tablename__ = 'find_events'
    id = Column(Integer, primary_key=True)
    tool_id = Column(String)
    timestamp = Column(DateTime)
    message = Column(String)
    finder_id = Column(String)
    location = Column(String)
    image_url = Column(String)
    image_filename = Column(String)
    thread_id = Column(String)
    reconnect_id = Column(String)
    notified = Column(Boolean, default=False)

# ✅ URIs from environment
sqlite_uri = os.getenv('SQLITE_DATABASE_URI')
postgres_uri = os.getenv('SQLALCHEMY_DATABASE_URI')

print("📦 Migrating data from:")
print(f"SQLite → {sqlite_uri}")
print(f"PostgreSQL → {postgres_uri}")

# ✅ Create engines/sessions
sqlite_engine = create_engine(sqlite_uri)
postgres_engine = create_engine(postgres_uri)

SQLiteSession = sessionmaker(bind=sqlite_engine)
PostgresSession = sessionmaker(bind=postgres_engine)

sqlite_session = SQLiteSession()
postgres_session = PostgresSession()

# ✅ Create tables in Postgres
print("🛠️ Creating tables in PostgreSQL...")
db.metadata.create_all(postgres_engine)

try:
    print("🔄 Migrating Devices...")
    for d in sqlite_session.query(LegacyDevice).all():
        new_device = Device(tool_id=d.tool_id, name=d.name)
        postgres_session.add(new_device)

    print("🔄 Migrating Find Events...")
    for e in sqlite_session.query(LegacyFindEvent).all():
        new_event = FindEvent(
            tool_id=e.tool_id,
            timestamp=e.timestamp,
            message=e.message,
            finder_id=e.finder_id,
            location=e.location,
            image_url=e.image_url,
            image_filename=e.image_filename,
            thread_id=e.thread_id,
            reconnect_id=e.reconnect_id,
            notified=e.notified,
        )
        postgres_session.add(new_event)

    postgres_session.commit()
    print("✅ Migration complete.")

except Exception as e:
    postgres_session.rollback()
    print(f"❌ Error during migration: {e}")

finally:
    sqlite_session.close()
    postgres_session.close()
