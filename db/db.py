"""
Инициализация объектов базы данных
"""
import warnings
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

import config

warnings.filterwarnings("ignore")

DB_URL = f"sqlite+aiosqlite:///{config.DB_FILE}"
async_engine = create_async_engine(url=DB_URL, echo=config.DB_ECHO)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

metadata = MetaData()
Base = declarative_base(bind=async_engine, metadata=metadata)

warnings.filterwarnings("default")
