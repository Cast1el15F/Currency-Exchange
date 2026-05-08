"""Модели даных о пользователях для бд"""

from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Users(Base):
    """Модель данных  пользователях для бд"""
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
