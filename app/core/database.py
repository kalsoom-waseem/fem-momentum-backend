"""
database.py
-----------
Database engine and session management.

Key ideas:
- Engine = manages DB connections
- Session = one unit of work (per request)
- Alembic owns schema changes (NOT this file)
"""

from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

# Database engine (connection factory)
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # enable SQL logs for development; disable in production
)

def get_session():
    """
    Yields a database session.
    One session is used per request and closed automatically.
    """
    with Session(engine) as session:
        yield session
