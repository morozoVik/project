import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_to_rub(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли, учитывая структуру из operations.json.
    """
    if not isinstance(transaction, dict):
        raise ValueError("Транзакция должна быть словарём")

    # Проверяем наличие operationAmount и вложенных полей
    try:
        operation_amount = transaction["operationAmount"]
        amount_str = operation_amount["amount"]
        currency_code = operation_amount["currency"]["code"].upper()
    except KeyError as e:
        raise ValueError(f"Отсутствует обязательное поле: {e}")

    # Преобразуем amount в число
    try:
        amount = float(amount_str)
    except (TypeError, ValueError):
        raise ValueError("Сумма транзакции должна быть числом")

    # Если валюта RUB, возвращаем как есть
    if currency_code == "RUB":
        return round(amount, 2)

    # Проверяем поддерживаемые валюты (USD, EUR)
    supported_currencies = {"USD", "EUR"}
    if currency_code not in supported_currencies:
        raise ValueError(f"Неподдерживаемая валюта: {currency_code}")

    # Получаем API-ключ из .env
    api_key = os.getenv("APILAYER_KEY")
    if not api_key:
        raise ValueError("Не настроен API-ключ (APILAYER_KEY)")

    # Конвертируем через API
    try:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_code}&amount={amount}"
        response = requests.get(url, headers={"apikey": api_key}, timeout=10)
        response.raise_for_status()
        result = response.json()
        return round(float(result["result"]), 2)
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Ошибка API: {e}")
    except (KeyError, ValueError) as e:
        raise ValueError(f"Ошибка обработки ответа API: {e}")
