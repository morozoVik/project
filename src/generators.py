def filter_by_currency(transactions: list[dict], currency: str) -> iter:
    """
    Фильтрует транзакции по заданной валюте и возвращает итератор.
    """
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        transaction_currency = operation_amount.get("currency", {}).get("code")
        if transaction_currency == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict]) -> iter:
    """
    Генератор, который последовательно возвращает описания транзакций.
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> iter:
    """
    Генератор номеров банковских карт в заданном диапазоне.
    """
    if start > end:
        raise ValueError("Начальное значение не может быть больше конечного")

    for number in range(start, end + 1):
        # Форматируем число в 16-значный номер с ведущими нулями
        card_number = f"{number:016d}"
        # Разбиваем на группы по 4 цифры с пробелами
        formatted_number = " ".join([card_number[i : i + 4] for i in range(0, 16, 4)])
        yield formatted_number
