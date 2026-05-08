"""Эндпоинты связанные с курсами валют"""

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request
from app.api.models.user import User
from app.core.security import get_user_from_token
from app.utils.external_api import Currency_Tools
from app.api.models.currency import Currency


currency_rourer = APIRouter(prefix="/currency", tags=["Currency"])


@currency_rourer.get("/get_all_currency_rates/{base_currency}")
async def get_all_currency(base_currency: str, user = Depends(get_user_from_token)) -> dict[str, Any]:
    """Получаем цены всех валют, в выбранной валюье"""
    if not user:
        raise HTTPException(status_code=401)
    print(user)
    return Currency_Tools(base_currency=base_currency).get_all_currency_rates()


@currency_rourer.get("/get_currency_rate/{base_currency.name}${to_currency.name}")
async def get_currency_rate(base_currency: Currency, to_currency: Currency, user: User = Depends(get_user_from_token)) -> dict[str, Any]:
    """Получаем цену to_currency в from_currency"""
    if not user:
        raise HTTPException(status_code=401)
    return Currency_Tools(base_currency=base_currency).get_currency_rate(to_currency = to_currency)