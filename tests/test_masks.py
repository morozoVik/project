import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize("card_number, expected", [
    ("1234567890123456", "1234 56** **** 3456"),
    ("1234567812345678", "1234 56** **** 5678"),
    ("1234", "1234"),  # граничный случай - короткий номер
    ("", ""),  # пустая строка
])
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("account_number, expected", [
    ("12345678901234567890", "**7890"),
    ("123456", "**3456"),  # граничный случай - короткий номер
    ("", "**"),  # пустая строка
])
def test_get_mask_account(account_number, expected):
    assert get_mask_account(account_number) == expected