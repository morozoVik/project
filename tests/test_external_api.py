from unittest.mock import MagicMock, patch

import pytest
import requests

from src.external_api import convert_to_rub


@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.json.return_value = {"result": 75.50}
    mock.raise_for_status.return_value = None
    return mock


def test_convert_rub_no_api_call():
    """Тест для рублевых транзакций (без вызова API)"""
    transaction = {"amount": "100.50", "currency": "RUB"}
    assert convert_to_rub(transaction) == 100.50


def test_convert_usd_success(mock_response):
    """Успешная конвертация USD в RUB"""
    with patch("requests.get", return_value=mock_response):
        transaction = {"amount": 100, "currency": "USD"}
        assert convert_to_rub(transaction) == 75.50


def test_convert_eur_success(mock_response):
    """Успешная конвертация EUR в RUB"""
    mock_response.json.return_value = {"result": 85.30}
    with patch("requests.get", return_value=mock_response):
        transaction = {"amount": "50", "currency": "EUR"}
        assert convert_to_rub(transaction) == 85.30


def test_convert_api_error():
    """Обработка ошибки API"""
    with patch(
        "requests.get", side_effect=requests.exceptions.RequestException("API error")
    ):
        with pytest.raises(ValueError, match="Ошибка API"):
            convert_to_rub({"amount": 100, "currency": "USD"})


@pytest.mark.parametrize(
    "transaction",
    [
        {"currency": "USD"},  # Нет amount
        {"amount": "invalid"},  # Нечисловой amount
        {"amount": 100, "currency": "XX"},  # Неверный код валюты
    ],
)
def test_convert_invalid_input(transaction):
    """Тест на невалидные входные данные"""
    with pytest.raises(ValueError):
        convert_to_rub(transaction)


def test_convert_missing_api_key(monkeypatch):
    """Тест на отсутствие API-ключа"""
    monkeypatch.delenv("APILAYER_KEY", raising=False)
    with patch("requests.get") as mock_get:
        with pytest.raises(ValueError, match="Не настроен API ключ"):
            convert_to_rub({"amount": 100, "currency": "USD"})
        mock_get.assert_not_called()  # Дополнительная проверка, что запрос не отправлялся
