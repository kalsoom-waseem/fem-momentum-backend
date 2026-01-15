"""
database.py
-----------
Database setup and session management.

- Creates the SQLAlchemy/SQLModel engine using DATABASE_URL
- Initializes database tables on application startup (for local dev)
- Provides a session generator for dependency injection

Key ideas:
- Engine = database connection manager
- Session = unit of work (one per request)
- Sessions are created and closed safely via FastAPI dependencies
"""


from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # shows SQL in terminal (great for learning)
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
