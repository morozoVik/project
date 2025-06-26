import pytest
from datetime import datetime
from your_module import filter_by_state, sort_by_date


# Фикстуры с тестовыми данными
@pytest.fixture
def sample_transactions():
    """Базовая фикстура с операциями разных статусов и дат"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T12:00:00.000"},
        {"id": 2, "state": "PENDING", "date": "2023-01-10T08:30:00.000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-20T15:45:00.000"},
        {"id": 4, "state": "CANCELED", "date": "2023-01-05T10:15:00.000"},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-25T09:00:00.000"},
    ]


@pytest.fixture
def transactions_with_same_dates():
    """Фикстура с операциями с одинаковыми датами"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T12:00:00.000"},
        {"id": 2, "state": "PENDING", "date": "2023-01-15T12:00:00.000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-15T12:00:00.000"},
    ]


@pytest.fixture
def transactions_with_invalid_dates():
    """Фикстура с операциями с некорректными датами"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15"},
        {"id": 2, "state": "PENDING", "date": "invalid-date"},
        {"id": 3, "state": "EXECUTED", "date": "15/01/2023"},
    ]


@pytest.fixture
def transactions_without_state():
    """Фикстура с операциями без поля state"""
    return [
        {"id": 1, "date": "2023-01-15T12:00:00.000"},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-10T08:30:00.000"},
    ]


# Параметризованные тесты для filter_by_state
@pytest.mark.parametrize("state,expected_ids", [
    ("EXECUTED", [1, 3, 5]),  # Стандартный случай
    ("PENDING", [2]),         # Одна операция
    ("CANCELED", [4]),        # Одна операция
    ("INVALID", []),          # Нет операций
    ("", []),                 # Пустой статус
])
def test_filter_by_state(sample_transactions, state, expected_ids):
    """Параметризованный тест фильтрации по разным статусам"""
    result = filter_by_state(sample_transactions, state)
    assert [op["id"] for op in result] == expected_ids


def test_filter_empty_list():
    """Тест фильтрации пустого списка"""
    assert filter_by_state([], "EXECUTED") == []


def test_filter_missing_state_field(transactions_without_state):
    """Тест фильтрации при отсутствии поля state"""
    result = filter_by_state(transactions_without_state, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 2


# Тесты для sort_by_date
def test_sort_descending(sample_transactions):
    """Тест сортировки по убыванию даты"""
    result = sort_by_date(sample_transactions)
    assert [op["id"] for op in result] == [5, 3, 1, 2, 4]


def test_sort_ascending(sample_transactions):
    """Тест сортировки по возрастанию даты"""
    result = sort_by_date(sample_transactions, reverse=False)
    assert [op["id"] for op in result] == [4, 2, 1, 3, 5]


def test_sort_same_dates(transactions_with_same_dates):
    """Тест сортировки при одинаковых датах (должны сохранить порядок)"""
    result = sort_by_date(transactions_with_same_dates)
    assert [op["id"] for op in result] == [1, 2, 3]


def test_sort_empty_list():
    """Тест сортировки пустого списка"""
    assert sort_by_date([]) == []


def test_sort_single_element():
    """Тест сортировки списка с одним элементом"""
    transactions = [{"date": "2023-01-01T00:00:00.000"}]
    assert sort_by_date(transactions) == transactions


def test_sort_missing_date_field():
    """Тест сортировки при отсутствии поля date"""
    transactions = [
        {"date": "2023-01-02T00:00:00.000"},
        {"no_date": True},
        {"date": "2023-01-01T00:00:00.000"}
    ]
    with pytest.raises(KeyError):
        sort_by_date(transactions)


def test_sort_invalid_date_format(transactions_with_invalid_dates):
    """Тест сортировки с некорректными форматами дат"""
    with pytest.raises(ValueError):
        sort_by_date(transactions_with_invalid_dates)


# Комбинированные тесты
def test_filter_and_sort_combined(sample_transactions):
    """Тест комбинированного использования фильтрации и сортировки"""
    filtered = filter_by_state(sample_transactions, "EXECUTED")
    sorted_ops = sort_by_date(filtered)
    assert [op["id"] for op in sorted_ops] == [5, 3, 1]


# Тесты на покрытие крайних случаев
def test_filter_none_state():
    """Тест фильтрации при передаче None в качестве статуса"""
    transactions = [
        {"id": 1, "state": None, "date": "2023-01-15T12:00:00.000"},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-10T08:30:00.000"},
    ]
    result = filter_by_state(transactions, None)
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_sort_with_timezones():
    """Тест сортировки с датами в разных часовых поясах"""
    transactions = [
        {"date": "2023-01-01T12:00:00.000+03:00"},
        {"date": "2023-01-01T10:00:00.000+01:00"},  # То же самое время
        {"date": "2023-01-01T09:00:00.000Z"},
    ]
    result = sort_by_date(transactions)
    assert [op["date"] for op in result] == [
        "2023-01-01T12:00:00.000+03:00",
        "2023-01-01T10:00:00.000+01:00",
        "2023-01-01T09:00:00.000Z",
    ]