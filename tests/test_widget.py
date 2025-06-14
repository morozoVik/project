import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("Счет 12345678901234567890", "Счет **7890"),
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
        ("Счет 123", "Счет **123"),  # Граничный случай - короткий номер
        ("Неизвестный тип 12345", "Неизвестный тип 12345"),  # Некорректные данные
    ],
)
def test_mask_account_card(input_str, expected):
    """
    Тестирование функции автоматического определения типа (карта/счет) и маскирования.
    """
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2018-07-11T02:26:18.671407", "11.07.2018"),  # Стандартный случай
        ("2020-01-01T00:00:00.000000", "01.01.2020"),  # Граничная дата
        ("invalid-date", "invalid-date"),  # Некорректный формат
    ],
)
def test_get_date(input_date, expected):
    """
    Тестирование функции форматирования даты.
    """
    assert get_date(input_date) == expected
