"""
Модель БД
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, func

from .db import Base


class Link(Base):
    """
    Ссылка по которой проходил пользователь
    """
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    link = Column(String())
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now(), nullable=False)

    def __str__(self):
        return f"Link(id={self.id}, link={self.chat_id})"

    def __repr__(self):
        return str(self)
