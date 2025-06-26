def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, оставляя первые 6 и последние 4 цифры видимыми.
    Остальные цифры заменяются на звездочки, с группировкой по 4 цифры.
    """
    # Проверяем, что номер карты состоит из 16 цифр (без пробелов)
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен состоять из 16 цифр")

    # Разбиваем номер на части: первые 6 и последние 4 цифры
    first_part = card_number[:4]  # Первые 4 цифры
    second_part = card_number[4:6]  # Следующие 2 цифры (5-6 цифры)
    last_part = card_number[-4:]  # Последние 4 цифры

    # Собираем замаскированную строку
    masked_number = f"{first_part} {second_part}** **** {last_part}"
    return masked_number


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета, оставляя видимыми только последние 4 цифры.
    Первые цифры заменяются на две звездочки.
    """
    # Проверяем, что номер счета содержит хотя бы 4 цифры
    if len(account_number) < 4 or not account_number.isdigit():
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    # Берем только последние 4 цифры номера
    last_digits = account_number[-4:]

    # Собираем замаскированную строку
    masked_account = f"**{last_digits}"
    return masked_account
