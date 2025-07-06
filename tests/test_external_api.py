import pytest
from unittest.mock import patch, MagicMock
import os
import requests
from src.external_api import convert_to_rub


@pytest.fixture
def mock_requests_get():
    with patch("src.external_api.requests.get") as mock_get:
        yield mock_get


@pytest.fixture
def mock_os_getenv():
    with patch("src.external_api.os.getenv") as mock_getenv:
        yield mock_getenv


def test_convert_to_rub_invalid_input_not_dict():
    """Тест на неверный тип ввода (не словарь)"""
    with pytest.raises(ValueError, match="Транзакция должна быть словарём"):
        convert_to_rub("not a dict")


def test_convert_to_rub_missing_operation_amount():
    """Тест на отсутствие обязательного поля operationAmount"""
    transaction = {}
    with pytest.raises(ValueError, match="Отсутствует обязательное поле: 'operationAmount'"):
        convert_to_rub(transaction)


def test_convert_to_rub_missing_amount():
    """Тест на отсутствие поля amount"""
    transaction = {"operationAmount": {}}
    with pytest.raises(ValueError, match="Отсутствует обязательное поле: 'amount'"):
        convert_to_rub(transaction)


def test_convert_to_rub_missing_currency_code():
    """Тест на отсутствие поля currency.code"""
    transaction = {"operationAmount": {"amount": "100", "currency": {}}}
    with pytest.raises(ValueError, match="Отсутствует обязательное поле: 'code'"):
        convert_to_rub(transaction)


def test_convert_to_rub_invalid_amount_format():
    """Тест на неверный формат суммы"""
    transaction = {
        "operationAmount": {
            "amount": "not a number",
            "currency": {"code": "USD"}
        }
    }
    with pytest.raises(ValueError, match="Сумма транзакции должна быть числом"):
        convert_to_rub(transaction)


def test_convert_to_rub_rub_currency():
    """Тест на транзакцию в рублях (должна возвращаться как есть)"""
    transaction = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"code": "RUB"}
        }
    }
    assert convert_to_rub(transaction) == 100.50


def test_convert_to_rub_unsupported_currency():
    """Тест на неподдерживаемую валюту"""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "GBP"}
        }
    }
    with pytest.raises(ValueError, match="Неподдерживаемая валюта: GBP"):
        convert_to_rub(transaction)


def test_convert_to_rub_missing_api_key(mock_os_getenv):
    """Тест на отсутствие API-ключа"""
    mock_os_getenv.return_value = None
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }
    with pytest.raises(ValueError, match=r"Не настроен API-ключ \(APILAYER_KEY\)"):
        convert_to_rub(transaction)


def test_convert_to_rub_api_success_usd(mock_os_getenv, mock_requests_get):
    """Тест успешной конвертации USD через API"""
    mock_os_getenv.return_value = "test-api-key"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 7500.50}
    mock_requests_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }

    result = convert_to_rub(transaction)
    assert result == 7500.50
    mock_requests_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100.0",
        headers={"apikey": "test-api-key"},
        timeout=10
    )


def test_convert_to_rub_api_success_eur(mock_os_getenv, mock_requests_get):
    """Тест успешной конвертации EUR через API"""
    mock_os_getenv.return_value = "test-api-key"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 8500.75}
    mock_requests_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "EUR"}
        }
    }

    result = convert_to_rub(transaction)
    assert result == 8500.75
    mock_requests_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount=100.0",
        headers={"apikey": "test-api-key"},
        timeout=10
    )


def test_convert_to_rub_api_failure(mock_os_getenv, mock_requests_get):
    """Тест ошибки API"""
    mock_os_getenv.return_value = "test-api-key"
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("API error")
    mock_requests_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "EUR"}
        }
    }

    with pytest.raises(ValueError, match="Ошибка API: API error"):
        convert_to_rub(transaction)


def test_convert_to_rub_api_invalid_response(mock_os_getenv, mock_requests_get):
    """Тест на неверный формат ответа API"""
    mock_os_getenv.return_value = "test-api-key"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}  # Нет поля result
    mock_requests_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }

    with pytest.raises(ValueError, match="Ошибка обработки ответа API"):
        convert_to_rub(transaction)


def test_convert_to_rub_api_timeout(mock_os_getenv, mock_requests_get):
    """Тест на таймаут запроса к API"""
    mock_os_getenv.return_value = "test-api-key"
    mock_requests_get.side_effect = requests.exceptions.Timeout("Request timeout")

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }

    with pytest.raises(ValueError, match="Ошибка API: Request timeout"):
        convert_to_rub(transaction)


def test_convert_to_rub_api_connection_error(mock_os_getenv, mock_requests_get):
    """Тест на ошибку соединения с API"""
    mock_os_getenv.return_value = "test-api-key"
    mock_requests_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }

    with pytest.raises(ValueError, match="Ошибка API: Connection failed"):
        convert_to_rub(transaction)