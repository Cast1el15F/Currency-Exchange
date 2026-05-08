"""Общие инструменты для работы с бд"""

from sqlalchemy.exc import IntegrityError
from typing import Any

from fastapi import HTTPException
import sqlalchemy
from app.api.models.user import User, UserSchema
from app.db.database import async_session_maker
from sqlalchemy import insert, select


class BaseDAO:
    """Общие инструменты для работы с бд. Используется как родительский класс"""
    model = None

    @classmethod
    async def find_all(cls) -> list[UserSchema]:
        """Возвращает все объекты из бд"""
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_by_filter(cls, **filter_by) -> list[UserSchema]:
        """Возвращает объект из бд по фильтрам"""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
    
    @classmethod
    async def find_one_or_none(cls, **filter_by) -> list[UserSchema]:
        """Возвращает объект из бд по фильтрам или не возвращает ничего"""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def add(cls, **data) -> None:
        """Добавляет объект в бд"""
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**data)
                await session.execute(query)
                await session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="User already exists"
            )