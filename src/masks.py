import logging


def setup_logger():
    """Настройка логгера для модуля masks"""
    logger = logging.getLogger("masks")
    logger.setLevel(logging.DEBUG)

    # Файловый обработчик с перезаписью при каждом запуске
    file_handler = logging.FileHandler("logs/masks.log", mode="w")
    file_handler.setLevel(logging.DEBUG)

    # Форматтер
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


logger = setup_logger()


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, оставляя первые 6 и последние 4 цифры видимыми.
    Остальные цифры заменяются на звездочки, с группировкой по 4 цифры.
    """
    try:
        logger.info(f"Начало маскировки номера карты: {card_number}")
        # Проверяем, что номер карты состоит из 16 цифр (без пробелов)
        if len(card_number) != 16 or not card_number.isdigit():
            error_msg = "Номер карты должен состоять из 16 цифр"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Разбиваем номер на части: первые 6 и последние 4 цифры
        first_part = card_number[:4]  # Первые 4 цифры
        second_part = card_number[4:6]  # Следующие 2 цифры (5-6 цифры)
        last_part = card_number[-4:]  # Последние 4 цифры

        # Собираем замаскированную строку
        masked_number = f"{first_part} {second_part}** **** {last_part}"
        logger.info(f"Успешная маскировка номера карты: {masked_number}")
        return masked_number
    except Exception as e:
        logger.exception(f"Ошибка при маскировке номера карты: {str(e)}")
        raise


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета, оставляя видимыми только последние 4 цифры.
    Первые цифры заменяются на две звездочки.
    """
    try:
        logger.info(f"Начало маскировки номера счета: {account_number}")
        # Проверяем, что номер счета содержит хотя бы 4 цифры
        if len(account_number) < 4 or not account_number.isdigit():
            error_msg = "Номер счета должен содержать минимум 4 цифры"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Берем только последние 4 цифры номера
        last_digits = account_number[-4:]

        # Собираем замаскированную строку
        masked_account = f"**{last_digits}"
        logger.info(f"Успешная маскировка номера счета: {masked_account}")
        return masked_account
    except Exception as e:
        logger.exception(f"Ошибка при маскировке номера счета: {str(e)}")
        raise
