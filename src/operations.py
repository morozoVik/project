import re
from collections import Counter
from typing import Dict, List


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Ищет транзакции, в описании которых встречается заданная строка (с учетом регистра).
    """
    if not search:
        return data

    result = []
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    for transaction in data:
        if "description" in transaction and pattern.search(transaction["description"]):
            result.append(transaction)
    return result


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций по заданным категориям.
    """
    descriptions = [t.get("description", "").lower() for t in data]
    category_counts = Counter(descriptions)
    return {
        cat: category_counts[cat.lower()]
        for cat in categories
        if cat.lower() in category_counts
    }
