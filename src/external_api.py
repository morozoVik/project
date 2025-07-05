import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_to_rub(transaction: Dict) -> float:
    """Конвертирует сумму транзакции в рубли по текущему курсу через API."""
    amount = transaction.get("amount")
    if amount is None:
        raise ValueError("Транзакция должна содержать сумму (amount)")

    currency = transaction.get("currency", "RUB").upper()

    if currency == "RUB":
        return round(float(amount), 2)

    api_key = os.getenv("APILAYER_KEY")
    if not api_key:
        raise ValueError("Не настроен API ключ")

    try:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
        response = requests.get(url, headers={"apikey": api_key}, timeout=10)
        response.raise_for_status()
        return round(response.json()["result"], 2)
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Ошибка API: {str(e)}")
