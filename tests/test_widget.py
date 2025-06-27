import pytest
from datetime import datetime
from src.widget import mask_account_card, get_date


# Фикстуры для тестов mask_account_card
@pytest.fixture
def valid_card_data():
    return [
        "Visa Platinum 7000792289606361",
        "Maestro 1596837868705199",
        "MasterCard 7158300734726758",
    ]


@pytest.fixture
def valid_account_data():
    return ["Счет 64686473678894779589", "Счет 35383033474447895560"]


@pytest.fixture
def invalid_data():
    return ["", "Неизвестный тип 1234567890", "Счет1234567890", "Карта", "Счет "]


# Фикстуры для тестов get_date
@pytest.fixture
def valid_date_data():
    return ["2019-07-03T18:35:29.512364", "2018-06-30T02:08:58.425572"]


@pytest.fixture
def invalid_date_data():
    return ["", "2023-13-01T00:00:00", "не дата", "2020-02-30T00:00:00"]


# Тесты для mask_account_card
@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
    ],
)
def test_mask_account_card_valid(input_data, expected):
    """Проверка корректной маскировки карт и счетов."""
    assert mask_account_card(input_data) == expected


def test_mask_account_card_invalid(invalid_data):
    """Проверка обработки некорректных данных."""
    for data in invalid_data:
        result = mask_account_card(data)
        if not data.strip():
            assert result == data
        elif data.startswith("Счет") and not data.startswith("Счет "):
            assert result == data
        else:
            assert result == data


# Тесты для get_date
@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2018-06-30T02:08:58.425572", "30.06.2018"),
    ],
)
def test_get_date_valid(input_data, expected):
    """Проверка корректного преобразования даты."""
    assert get_date(input_data) == expected


def test_get_date_invalid(invalid_date_data):
    """Проверка обработки некорректных дат."""
    for data in invalid_date_data:
        result = get_date(data)
        if not data:
            assert result == ""
        else:
            try:
                datetime.fromisoformat(data)
                assert True
            except ValueError:
                assert result == ""


# Дополнительные тесты для покрытия всех ветвей
def test_mask_account_card_edge_cases():
    """Проверка граничных случаев для mask_account_card."""
    assert mask_account_card("Счет ") == "Счет "
    assert mask_account_card("Карта 1234") == "Карта 1234"
    assert mask_account_card("") == ""
    assert mask_account_card("   ") == "   "


def test_get_date_edge_cases():
    """Проверка граничных случаев для get_date."""
    assert get_date("") == ""
    assert get_date("2020-02-30T00:00:00") == ""