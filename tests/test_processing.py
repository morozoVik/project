import pytest

from src.processing import filter_by_state, sort_by_date


# Фикстуры с тестовыми данными
@pytest.fixture
def transaction_data():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-04-16T08:45:00.000"},
        {"id": 2, "state": "PENDING", "date": "2023-04-15T10:15:00.000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-04-16T08:45:00.000"},
        {"id": 4, "state": "CANCELED", "date": "2023-04-14T18:20:00.000"},
        {"id": 5, "state": None, "date": "2023-04-13T09:10:00.000"},
    ]


@pytest.fixture
def edge_case_data():
    return [
        {"id": 1, "date": "2023-01-01"},  # нет state
        {"id": 2},  # нет state и date
        {"id": 3, "state": "EXECUTED"},  # нет date
    ]


# Параметризованные тесты для filter_by_state
@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("PENDING", [2]),
        ("NON_EXISTENT", []),
    ],
)
def test_filter_by_state(transaction_data, state, expected_ids):
    result = filter_by_state(transaction_data, state)
    assert [x["id"] for x in result] == expected_ids


def test_filter_by_state_edge_cases(edge_case_data):
    assert len(filter_by_state(edge_case_data, "EXECUTED")) == 1


# Параметризованные тесты для sort_by_date
@pytest.mark.parametrize(
    "reverse, first_id",
    [
        (True, 1),  # по убыванию
        (False, 5),  # по возрастанию
    ],
)
def test_sort_by_date(transaction_data, reverse, first_id):
    result = sort_by_date(transaction_data, reverse)
    assert result[0]["id"] == first_id


def test_sort_by_date_edge_cases(edge_case_data):
    with pytest.raises(KeyError):
        sort_by_date(edge_case_data)
