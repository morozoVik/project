def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в переданной строке."""
    if not account_info.strip():
        return account_info  # Возвращаем пустую строку или строку с пробелами без изменений

    parts = account_info.split()
    if not parts:
        return account_info

    # Определяем, это карта или счет
    if parts[0] == "Счет":
        if len(parts) < 2:
            return account_info  # Нет номера счета
        account_number = parts[-1]
        if len(account_number) < 4:
            return account_info  # Номер счета слишком короткий
        masked_number = f"**{account_number[-4:]}"
        return f"{parts[0]} {masked_number}"
    else:
        if len(parts) < 2:
            return account_info  # Нет номера карты
        card_number = parts[-1]
        if len(card_number) < 16:
            return account_info  # Номер карты слишком короткий
        masked_number = (
            f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        )
        return " ".join(parts[:-1] + [masked_number])


def get_date(date_str: str) -> str:
    """Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ."""
    from datetime import datetime

    if not date_str:
        return ""

    try:
        date_obj = datetime.fromisoformat(date_str)
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        return ""  # Или можно вернуть исходную строку, или поднять исключение
