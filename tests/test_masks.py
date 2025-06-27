import pytest

from src.masks import get_mask_card_number, get_mask_account


# Фикстуры с тестовыми данными
@pytest.fixture
def valid_card_numbers():
    return ["1234567890123456", "9876543210987654", "1111222233334444"]


@pytest.fixture
def invalid_card_numbers():
    return [
        "1234567890",  # слишком короткий
        "12345678901234567890",  # слишком длинный
        "1234abcd90123456",  # содержит буквы
        "1234 5678 9012 3456",  # содержит пробелы
    ]


@pytest.fixture
def valid_account_numbers():
    return ["1234567890", "9876543210", "0000123456"]


@pytest.fixture
def invalid_account_numbers():
    return [
        "123",  # слишком короткий
        "",  # пустая строка
        "12ab",  # содержит буквы
        "123 456",  # содержит пробелы
    ]


# Параметризованные тесты для get_mask_card_number
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("9876543210987654", "9876 54** **** 7654"),
        ("1111222233334444", "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number_valid(valid_card_numbers, card_number, expected):
    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_invalid(invalid_card_numbers):
    for number in invalid_card_numbers:
        with pytest.raises(ValueError):
            get_mask_card_number(number)


# Параметризованные тесты для get_mask_account
@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("1234567890", "**7890"),
        ("9876543210", "**3210"),
        ("0000123456", "**3456"),
    ],
)
def test_get_mask_account_valid(valid_account_numbers, account_number, expected):
    assert get_mask_account(account_number) == expected


def test_get_mask_account_invalid(invalid_account_numbers):
    for number in invalid_account_numbers:
        with pytest.raises(ValueError):
            get_mask_account(number)
