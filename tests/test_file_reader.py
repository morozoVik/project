from unittest.mock import patch

import pandas as pd
import pytest

from src.file_reader import read_csv_transactions, read_excel_transactions


@pytest.fixture
def sample_data():
    return [
        {"id": 1, "amount": 100, "currency": "RUB"},
        {"id": 2, "amount": 200, "currency": "USD"},
    ]


def test_read_csv_transactions_success(sample_data):
    """Тест успешного чтения CSV файла."""
    with patch("pathlib.Path.exists", return_value=True):
        with patch("pandas.read_csv") as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame(sample_data)
            result = read_csv_transactions("dummy.csv")

            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[1]["currency"] == "USD"


def test_read_excel_transactions_success(sample_data):
    """Тест успешного чтения Excel файла."""
    with patch("pathlib.Path.exists", return_value=True):
        with patch("pandas.read_excel") as mock_read_excel:
            mock_read_excel.return_value = pd.DataFrame(sample_data)
            result = read_excel_transactions("dummy.xlsx")

            assert len(result) == 2
            assert result[0]["amount"] == 100
            assert result[1]["id"] == 2


def test_read_csv_file_not_found():
    """Тест обработки отсутствующего файла."""
    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(ValueError, match="Ошибка при чтении CSV: Файл не найден"):
            read_csv_transactions("nonexistent.csv")


def test_read_excel_invalid_format():
    """Тест обработки неверного формата файла."""
    with patch("pathlib.Path.exists", return_value=True):
        with patch("pandas.read_excel") as mock_read_excel:
            mock_read_excel.side_effect = ValueError("Invalid file format")
            with pytest.raises(ValueError, match="Ошибка при чтении Excel"):
                read_excel_transactions("invalid.xlsx")
