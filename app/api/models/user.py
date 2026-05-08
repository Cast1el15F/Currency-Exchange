"""Модели данных связанные с пользователями"""

from pydantic import BaseModel


class User(BaseModel):
    """Информация о пользователях для аписи в бд"""
    name: str
    password: str


class UserSchema(BaseModel):
    """Информация о пользователях, возвращающаяся из бд"""
    id: int
    name: str
    password: str
