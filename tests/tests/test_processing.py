import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_transactions():
    """Фикстура предоставляет тестовый набор транзакций с разными статусами и датами."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2021-01-01T00:00:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2021-02-01T00:00:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2021-03-01T00:00:00.000000"},
        {"id": 4, "state": "PENDING", "date": "2021-04-01T00:00:00.000000"},
    ]


def test_filter_by_state(sample_transactions):
    """
    Тестирование фильтрации транзакций по статусу.
    """
    # Тестирование фильтрации по статусу EXECUTED
    result = filter_by_state(sample_transactions, "EXECUTED")
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)
    
    # Проверка, что исходный список не изменился
    assert len(sample_transactions) == 4
    
    # Тестирование фильтрации по несуществующему статусу
    result = filter_by_state(sample_transactions, "UNKNOWN")
    assert len(result) == 0


@pytest.mark.parametrize(
    "reverse, expected_order",
    [
        (False, [1, 3, 2, 4]),  # Сортировка по возрастанию даты
        (True, [4, 2, 3, 1]),   # Сортировка по убыванию даты
    ],
)
def test_sort_by_date(sample_transactions, reverse, expected_order):
    """
    Тестирование сортировки транзакций по дате.
    """
    result = sort_by_date(sample_transactions, reverse)
    assert [item["id"] for item in result] == expected_order
    assert len(result) == len(sample_transactions)  # Все элементы сохраняются


def test_sort_by_date_empty():
    """
    Тестирование обработки пустого списка транзакций.
    """
    assert sort_by_date([], True) == []