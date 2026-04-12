"""
Модуль для обработки финансовых операций.
Содержит функции для фильтрации и сортировки операций.
"""

from typing import List, Dict


def filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Фильтрует список операций по указанному статусу."""

    filtered_operations = []

    for operation in transactions:
        if operation.get("state") == state:
            filtered_operations.append(operation)

    return filtered_operations


def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Сортирует список операций по дате.

    Args:
        transactions: Список словарей с операциями.
        reverse: Порядок сортировки (True - новые сначала, False - старые сначала).

    Returns:
        Отсортированный список операций.

    Example:
        >>> ops = [{'date': '2023-01-01'}, {'date': '2023-01-02'}]
        >>> sort_by_date(ops)
        [{'date': '2023-01-02'}, {'date': '2023-01-01'}]
    """
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)
