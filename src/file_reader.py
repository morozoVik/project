import logging
from pathlib import Path
from typing import Dict, List

import pandas as pd

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/file_reader.log")
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(handler)


def read_csv_transactions(file_path: str) -> List[Dict]:
    """
    Читает транзакции из CSV файла.
    """
    try:
        logger.info(f"Чтение CSV файла: {file_path}")
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        df = pd.read_csv(file_path)
        transactions = df.to_dict("records")
        logger.info(f"Успешно прочитано {len(transactions)} транзакций")
        return transactions

    except pd.errors.EmptyDataError:
        logger.error("CSV файл пуст")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV: {str(e)}")
        raise ValueError(f"Ошибка при чтении CSV: {str(e)}") from e


def read_excel_transactions(file_path: str) -> List[Dict]:
    """
    Читает транзакции из Excel файла.
    """
    try:
        logger.info(f"Чтение Excel файла: {file_path}")
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        df = pd.read_excel(file_path)
        transactions = df.to_dict("records")
        logger.info(f"Успешно прочитано {len(transactions)} транзакций")
        return transactions

    except Exception as e:
        logger.error(f"Ошибка при чтении Excel: {str(e)}")
        raise ValueError(f"Ошибка при чтении Excel: {str(e)}") from e
