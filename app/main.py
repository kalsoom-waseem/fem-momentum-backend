"""
main.py
-------
Application entrypoint.

- Creates the FastAPI app instance
- Runs startup logic using lifespan (e.g. database initialization)
- Defines basic health check endpoint

This file is equivalent to `server.js` in Node/Express:
it wires everything together and starts the app.
"""


from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import init_db

from app.api.v1.router import router as v1_router
from app.models.profile import UserProfile  # noqa: F401



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once at startup (before handling requests)
    print("🚀 Starting application...")
    init_db()
    print("✅ Database connected and tables ready")
    yield
    print("🛑 Shutting down application...")


app = FastAPI(title="Fem Momentum", lifespan=lifespan)


app.include_router(v1_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
