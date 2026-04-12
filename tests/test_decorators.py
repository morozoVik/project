import os
from datetime import datetime

import pytest

from src.decorators import log


# Тестовая функция для проверки успешного выполнения
@log()
def successful_func(a, b):
    return a + b


# Тестовая функция для проверки ошибок
@log()
def failing_func(a, b):
    return a / b


def test_log_to_console_success(capsys):
    """Тест успешного выполнения с выводом в консоль"""
    result = successful_func(2, 3)

    captured = capsys.readouterr()
    output = captured.out

    assert result == 5
    assert "successful_func ok" in output
    assert "Result: 5" in output
    assert datetime.now().strftime("%Y-%m-%d") in output


def test_log_to_console_error(capsys):
    """Тест ошибки с выводом в консоль"""
    with pytest.raises(ZeroDivisionError):
        failing_func(1, 0)

    captured = capsys.readouterr()
    output = captured.err

    assert "failing_func error" in output
    assert "ZeroDivisionError" in output
    assert "Inputs: (1, 0)" in output


def test_log_to_file_success(tmp_path):
    """Тест успешного выполнения с выводом в файл"""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def file_log_func(x, y):
        return x * y

    result = file_log_func(3, 4)

    assert result == 12
    assert log_file.exists()

    with open(log_file, "r") as f:
        content = f.read()
        assert "file_log_func ok" in content
        assert "Result: 12" in content


def test_log_to_file_error(tmp_path):
    """Тест ошибки с выводом в файл"""
    log_file = tmp_path / "error_log.txt"

    @log(filename=str(log_file))
    def file_error_func(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        file_error_func(5, 0)

    assert log_file.exists()

    with open(log_file, "r") as f:
        content = f.read()
        assert "file_error_func error" in content
        assert "ZeroDivisionError" in content
        assert "Inputs: (5, 0)" in content


def test_log_preserves_function_metadata():
    """Тест сохранения метаданных функции"""

    @log()
    def metadata_test(a, b):
        """Test function"""
        return a + b

    assert metadata_test.__name__ == "metadata_test"
    assert metadata_test.__doc__ == "Test function"
    assert metadata_test.__module__ == __name__


def test_log_with_no_filename_uses_console(capsys):
    """Тест, что без filename используется консоль"""

    @log()
    def console_func(x):
        return x**2

    console_func(3)
    captured = capsys.readouterr()

    assert "console_func ok" in captured.out
    assert "Result: 9" in captured.out


def test_log_with_filename_creates_file(tmp_path):
    """Тест создания файла при указании filename"""
    log_file = tmp_path / "new_log.txt"

    @log(filename=str(log_file))
    def new_func():
        return "test"

    new_func()

    assert log_file.exists()
    assert os.path.getsize(log_file) > 0


def test_log_rethrows_exceptions():
    """Тест, что декоратор пробрасывает исключения"""

    @log()
    def exception_func():
        raise ValueError("Test error")

    with pytest.raises(ValueError) as exc_info:
        exception_func()

    assert "Test error" in str(exc_info.value)
