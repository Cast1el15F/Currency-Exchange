"""Инструменты для работы с таблицей Users"""

from app.api.models.user import User
from app.db.base import BaseDAO
from app.db.models.users import Users
from app.db.database import async_session_maker
from sqlalchemy import select


class UsersDAO(BaseDAO):
    """Методы как в родителе, только работает с моделью Users"""
    model = Users

    @classmethod
    async def update_user(cls, id: int | None = None, name: str | None = None, password: str | None = None) -> Users | None:
        """Обновляет пользователя по id или по имени.

        Найдет пользователя, изменит поля и сохранит изменения в базе.
        Возвращает обновленного пользователя, или None если не найден.
        """
        if id is None and name is None:
            return None

        async with async_session_maker() as session:
            user = None
            if id is not None:
                user = await session.get(cls.model, id)

            if user is None and name is not None:
                query = select(cls.model).filter_by(name=name)
                result = await session.execute(query)
                user = result.scalar_one_or_none()

            if user is None:
                return None

            # Меняем только те поля, которые переданы.
            if name is not None:
                user.name = name
            if password is not None:
                user.password = password

            await session.commit()
            await session.refresh(user)
            return user

    @classmethod
    async def delete_user(cls, id: int | None = None, name: str | None = None) -> bool:
        """Удаляет пользователя по id или по имени.

        Если пользователь найден, удаляет его и возвращает True.
        Если пользователь не найден, возвращает False.
        """
        if id is None and name is None:
            return False

        async with async_session_maker() as session:
            user = None
            if id is not None:
                user = await session.get(cls.model, id)

            if user is None and name is not None:
                query = select(cls.model).filter_by(name=name)
                result = await session.execute(query)
                user = result.scalar_one_or_none()

            if user is None:
                return False

            await session.delete(user)
            await session.commit()
            return True