import csv
import json
from typing import Dict, List

import openpyxl

from operations import process_bank_operations, process_bank_search
from utils import filter_by_status, filter_rub_only, sort_transactions


def load_json(file_path: str) -> List[Dict]:
    """Загружает данные из JSON-файла."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(file_path: str) -> List[Dict]:
    """Загружает данные из CSV-файла."""
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_xlsx(file_path: str) -> List[Dict]:
    """Загружает данные из XLSX-файла."""
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        data.append(dict(zip(headers, row)))
    return data


def print_transaction(transaction: Dict) -> None:
    """Выводит информацию о транзакции в консоль."""
    print(f"{transaction.get('date')} {transaction.get('description')}")
    print(f"Сумма: {transaction.get('amount')} {transaction.get('currency')}\n")


def print_operations_stats(data: List[Dict]) -> None:
    """Выводит статистику по операциям."""
    categories = ["Перевод", "Платеж", "Вклад", "Списание"]
    stats = process_bank_operations(data, categories)
    print("\nСтатистика по операциям:")
    for category, count in stats.items():
        print(f"{category}: {count} операций")


def main() -> None:
    """Основная логика программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ").strip()
    file_path = ""

    if choice == "1":
        file_path = "transactions.json"
        print("Для обработки выбран JSON-файл.")
        data = load_json(file_path)
    elif choice == "2":
        file_path = "transactions.csv"
        print("Для обработки выбран CSV-файл.")
        data = load_csv(file_path)
    elif choice == "3":
        file_path = "transactions.xlsx"
        print("Для обработки выбран XLSX-файл.")
        data = load_xlsx(file_path)
    else:
        print("Неверный выбор. Завершение программы.")
        return

    while True:
        status = (
            input(
                "Введите статус, по которому необходимо выполнить фильтрацию.\n"
                "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
            )
            .strip()
            .upper()
        )

        if status in ("EXECUTED", "CANCELED", "PENDING"):
            print(f"Операции отфильтрованы по статусу '{status}'")
            break
        print(f"Статус операции '{status}' недоступен.")

    filtered_data = filter_by_status(data, status)

    sort_choice = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
    if sort_choice == "да":
        sort_order = (
            input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        )
        reverse = sort_order == "по убыванию"
        filtered_data = sort_transactions(filtered_data, reverse)

    rub_only = input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()
    if rub_only == "да":
        filtered_data = filter_rub_only(filtered_data)

    search_choice = (
        input(
            "Отфильтровать список транзакций по определенному слову в описании? Да/Нет: "
        )
        .strip()
        .lower()
    )
    if search_choice == "да":
        search_word = input("Введите слово для поиска: ").strip()
        filtered_data = process_bank_search(filtered_data, search_word)

    print_operations_stats(filtered_data)

    print("\nРаспечатываю итоговый список транзакций...")
    if not filtered_data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"\nВсего банковских операций в выборке: {len(filtered_data)}")
        for transaction in filtered_data:
            print_transaction(transaction)


if __name__ == "__main__":
    main()
