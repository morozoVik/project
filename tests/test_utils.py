from unittest.mock import mock_open, patch

import pytest

from src.utils import get_transactions


@pytest.mark.parametrize(
    "file_content,expected",
    [
        ('[{"id": 1}]', [{"id": 1}]),  # Валидный JSON-список
        ('{"id": 1}', []),  # JSON-объект (не список)
        ("", []),  # Пустой файл
        ("invalid json", []),  # Невалидный JSON
    ],
)
def test_get_transactions(file_content, expected):
    with patch("builtins.open", mock_open(read_data=file_content)):
        result = get_transactions("dummy.json")
        assert result == expected


def test_get_transactions_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        assert get_transactions("nonexistent.json") == []
