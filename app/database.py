# Windows PowerShell: sobrescribe app/database.py con el contenido correcto
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/happinessdb")

# async engine para sesiones async
async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)

def create_db_and_tables():
    sync_url = DATABASE_URL.replace("+asyncpg", "")
    sync_engine = create_engine(sync_url)
    SQLModel.metadata.create_all(sync_engine)

