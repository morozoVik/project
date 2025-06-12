def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в переданной строке."""
    parts = account_info.split()
    # Определяем, это карта или счет
    if parts[0] == "Счет":
        # Маскируем счет
        account_number = parts[-1]
        masked_number = f"**{account_number[-4:]}"
        return f"{parts[0]} {masked_number}"
    else:
        # Маскируем карту
        card_number = parts[-1]
        masked_number = (
            f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        )
        return " ".join(parts[:-1] + [masked_number])


def get_date(date_str: str) -> str:
    """Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ."""
    from datetime import datetime

    date_obj = datetime.fromisoformat(date_str)
    return date_obj.strftime("%d.%m.%Y")
