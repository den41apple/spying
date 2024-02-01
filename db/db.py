"""
Инициализация объектов базы данных
"""
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

import config

async_engine = create_async_engine(url=config.DB_URL, echo=config.DB_ECHO)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

metadata = MetaData()
Base = declarative_base(bind=async_engine, metadata=metadata)
