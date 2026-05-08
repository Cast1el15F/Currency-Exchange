"""Модели данных связанные с валютами"""

from pydantic import BaseModel


class Currency(BaseModel):
    """Информация о валюте"""
    name: str