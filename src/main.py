import csv
import json
from pathlib import Path
from typing import Dict, List

import openpyxl

from operations import process_bank_operations, process_bank_search
from utils import filter_by_status, filter_rub_only, sort_transactions


def load_json(file_path: str) -> List[Dict]:
    """Загружает данные из JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден!")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {file_path} не является корректным JSON!")
        return []


def load_csv(file_path: str) -> List[Dict]:
    """Загружает данные из CSV-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден!")
        return []


def load_xlsx(file_path: str) -> List[Dict]:
    """Загружает данные из XLSX-файла."""
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        data = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(dict(zip(headers, row)))
        return data
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден!")
        return []


def print_transaction(transaction: Dict) -> None:
    """Выводит информацию о транзакции в консоль."""
    date = transaction.get("date", "Дата не указана")
    description = transaction.get("description", "Описание отсутствует")
    amount = transaction.get("amount", "Сумма не указана")
    currency = transaction.get("currency", "Валюта не указана")

    print(f"{date} {description}")
    print(f"Сумма: {amount} {currency}\n")


def print_operations_stats(data: List[Dict]) -> None:
    """Выводит статистику по операциям."""
    if not data:
        print("Нет данных для вывода статистики")
        return

    categories = ["Перевод", "Платеж", "Вклад", "Списание"]
    stats = process_bank_operations(data, categories)

    print("\nСтатистика по операциям:")
    for category, count in stats.items():
        print(f"- {category}: {count} операций")


def get_file_path(choice: str) -> str:
    """Возвращает путь к файлу в зависимости от выбора пользователя."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    if choice == "1":
        return str(data_dir / "transactions.json")
    elif choice == "2":
        return str(data_dir / "transactions.csv")
    elif choice == "3":
        return str(data_dir / "transactions.xlsx")
    return ""


def main() -> None:
    """Основная логика программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор файла
    while True:
        choice = input("Ваш выбор (1-3): ").strip()
        if choice in ("1", "2", "3"):
            break
        print("Пожалуйста, введите число от 1 до 3")

    file_path = get_file_path(choice)

    # Загрузка данных
    if choice == "1":
        print("\nДля обработки выбран JSON-файл.")
        data = load_json(file_path)
    elif choice == "2":
        print("\nДля обработки выбран CSV-файл.")
        data = load_csv(file_path)
    else:
        print("\nДля обработки выбран XLSX-файл.")
        data = load_xlsx(file_path)

    if not data:
        print("\nНе удалось загрузить данные. Программа завершена.")
        return

    # Фильтрация по статусу
    while True:
        print("\nДоступные статусы операций: EXECUTED, CANCELED, PENDING")
        status = (
            input("Введите статус для фильтрации (или Enter для всех): ")
            .strip()
            .upper()
        )

        if not status or status in ("EXECUTED", "CANCELED", "PENDING"):
            break
        print(f"Ошибка: статус '{status}' недоступен!")

    filtered_data = filter_by_status(data, status) if status else data

    if not filtered_data:
        print("\nНет операций с выбранным статусом.")
        return

    # Сортировка
    sort_choice = input("\nОтсортировать операции по дате? (да/нет): ").strip().lower()
    if sort_choice == "да":
        while True:
            sort_order = (
                input("Сортировать по возрастанию или убыванию? (возр/убыв): ")
                .strip()
                .lower()
            )
            if sort_order in ("возр", "убыв"):
                break
            print("Пожалуйста, введите 'возр' или 'убыв'")

        filtered_data = sort_transactions(filtered_data, reverse=(sort_order == "убыв"))

    # Фильтрация по валюте
    rub_only = (
        input("\nВыводить только рублевые транзакции? (да/нет): ").strip().lower()
    )
    if rub_only == "да":
        filtered_data = filter_rub_only(filtered_data)
        if not filtered_data:
            print("Нет рублевых транзакций в выборке.")
            return

    # Поиск по описанию
    search_choice = (
        input("\nИскать по ключевому слову в описании? (да/нет): ").strip().lower()
    )
    if search_choice == "да":
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            filtered_data = process_bank_search(filtered_data, search_word)
            if not filtered_data:
                print("Нет транзакций с таким словом в описании.")
                return

    # Вывод результатов
    print("\n" + "=" * 50)
    print_operations_stats(filtered_data)

    print("\nРезультаты фильтрации:")
    if not filtered_data:
        print("Нет транзакций, соответствующих вашим критериям.")
    else:
        print(f"\nНайдено операций: {len(filtered_data)}")
        for transaction in filtered_data:
            print_transaction(transaction)


if __name__ == "__main__":
    main()
