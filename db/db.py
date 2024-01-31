"""
Инициализация объектов базы данных
"""
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

import config


DB_URL = f"sqlite+aiosqlite:///data.db"

async_engine = create_async_engine(url=DB_URL, echo=False)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

metadata = MetaData()
Base = declarative_base(bind=async_engine, metadata=metadata)
