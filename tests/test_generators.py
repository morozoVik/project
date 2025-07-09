import pytest

from src.generators import (card_number_generator, filter_by_currency,
                            transaction_descriptions)


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "RUB", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]


def test_filter_by_currency_usd(sample_transactions):
    usd_transactions = filter_by_currency(sample_transactions, "USD")
    usd_transactions_list = list(usd_transactions)
    assert len(usd_transactions_list) == 2
    assert all(
        t["operationAmount"]["currency"]["code"] == "USD" for t in usd_transactions_list
    )


def test_filter_by_currency_rub(sample_transactions):
    rub_transactions = filter_by_currency(sample_transactions, "RUB")
    rub_transactions_list = list(rub_transactions)
    assert len(rub_transactions_list) == 1
    assert rub_transactions_list[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_by_currency_empty_list():
    empty_transactions = []
    usd_transactions = filter_by_currency(empty_transactions, "USD")
    assert list(usd_transactions) == []


def test_filter_by_currency_no_matching(sample_transactions):
    eur_transactions = filter_by_currency(sample_transactions, "EUR")
    assert list(eur_transactions) == []


def test_transaction_descriptions(sample_transactions):
    descriptions = transaction_descriptions(sample_transactions)
    expected_descriptions = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
    ]
    assert list(descriptions) == expected_descriptions


def test_transaction_descriptions_empty_list():
    empty_transactions = []
    descriptions = transaction_descriptions(empty_transactions)
    assert list(descriptions) == []


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (
            9999_9999_9999_9998,
            9999_9999_9999_9999,
            ["9999 9999 9999 9998", "9999 9999 9999 9999"],
        ),
    ],
)
def test_card_number_generator(start, end, expected):
    card_numbers = list(card_number_generator(start, end))
    assert card_numbers == expected


def test_card_number_generator_formatting():
    card_numbers = card_number_generator(1234_5678_9012_3456, 1234_5678_9012_3456)
    assert next(card_numbers) == "1234 5678 9012 3456"


def test_card_number_generator_invalid_range():
    with pytest.raises(ValueError):
        list(card_number_generator(10_000_000_000_000_000, 1))
