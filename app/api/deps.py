"""
deps.py
-------
Shared FastAPI dependencies.

This file contains reusable dependencies that are injected
into endpoints using FastAPI's Depends system.

Currently:
- SessionDep → provides a database session (one per request)
"""

from typing import Annotated
from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session

# One DB session per request
SessionDep = Annotated[Session, Depends(get_session)]
