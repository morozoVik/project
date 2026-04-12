import json
import logging
from typing import Dict, List


def setup_logger():
    """Настройка логгера для модуля utils"""
    logger = logging.getLogger("utils")
    logger.setLevel(logging.DEBUG)

    # Файловый обработчик с перезаписью при каждом запуске
    file_handler = logging.FileHandler("logs/utils.log", mode="w")
    file_handler.setLevel(logging.DEBUG)

    # Форматтер
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


logger = setup_logger()


def get_transactions(file_path: str) -> List[Dict]:
    """Возвращает список транзакций из JSON-файла."""
    try:
        logger.info(f"Попытка загрузить транзакции из файла: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if not isinstance(data, list):
                logger.warning(f"Файл {file_path} не содержит список транзакций")
                return []

            logger.info(f"Успешно загружено {len(data)} транзакций")
            return data

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        return []
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при загрузке транзакций: {str(e)}")
        return []


def filter_by_status(data: List[Dict], status: str) -> List[Dict]:
    """
    Фильтрует транзакции по статусу.
    """
    if not status:
        return data
    return [t for t in data if t.get("state", "").upper() == status.upper()]


def sort_transactions(data: List[Dict], reverse: bool = False) -> List[Dict]:
    """
    Сортирует транзакции по дате.
    """
    return sorted(data, key=lambda x: x.get("date", ""), reverse=reverse)


def filter_rub_only(data: List[Dict]) -> List[Dict]:
    """
    Фильтрует транзакции, оставляя только рублевые.
    """
    return [t for t in data if t.get("currency", "").lower() == "rub"]
