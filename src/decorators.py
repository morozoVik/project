from datetime import datetime
from functools import wraps
import sys


def log(filename=None):
    """
    Декоратор для логирования выполнения функций.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Формируем информацию о вызове
            func_name = func.__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успехе
                log_message = f"{timestamp} - {func_name} ok. Result: {result}\n"

                if filename:
                    # Записываем в файл
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    # Выводим в консоль
                    print(log_message, end="")

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_message = (
                    f"{timestamp} - {func_name} error: {type(e).__name__}: {str(e)}. "
                    f"Inputs: {args}, {kwargs}\n"
                )

                if filename:
                    # Записываем в файл
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message)
                else:
                    # Выводим в консоль
                    print(error_message, end="", file=sys.stderr)

                raise  # Пробрасываем исключение дальше

        return wrapper

    return decorator