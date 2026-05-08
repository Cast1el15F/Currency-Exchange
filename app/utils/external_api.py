"""Работа с внешним апи currencyapi.net для получения курса валют"""

from typing import Any
import requests
from app.api.models.currency import Currency
from app.core.config import settings


class Currency_Tools:
    """Класс для работы с апи currencyapi.net"""

    def __init__(self, base_currency: Currency):
        self.url = "https://currencyapi.net/api/v2/rates"
        self.params = {
            "key": settings.api_key,
            "base": base_currency.upper(),
            "output": "JSON"
        }

    def get_all_currency_rates(self) -> dict[str: Any]:
        """Получаем цены всех валют, в выбранной валюье"""
        response = requests.get(self.url, params=self.params)
        data = response.json()
        return data
    
    def get_currency_rate(self, to_currency: Currency) -> float:
        """Получаем цену to_currency в from_currency"""
        all_currency = self.get_all_currency_rates()
        return all_currency["rates"][to_currency.name.upper()]