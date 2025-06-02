def get_mask_card_number(card_number: str) -> str:
    cleaned_number = card_number.replace(" ", "")

    # Проверяем, что номер карты состоит только из цифр и имеет корректную длину (16 цифр)
    if not cleaned_number.isdigit() or len(cleaned_number) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр")

    first_part = cleaned_number[:4]
    second_part = cleaned_number[4:6]
    last_part = cleaned_number[-4:]

    # Формируем замаскированную строку
    masked_number = f"{first_part} {second_part}** **** {last_part}"

    return masked_number


# Запрашиваем номер карты у пользователя
user_input = input("Введите номер карты (16 цифр): ")

try:
    masked_card = get_mask_card_number(user_input)
    print("Замаскированный номер карты:", masked_card)
except ValueError as e:
    print("Ошибка:", e)


def get_mask_account(account_number: str) -> str:
    # Удаляем все пробелы и преобразуем в строку (если вдруг передали число)
    cleaned_number = str(account_number).replace(" ", "")

    # Проверяем, что номер состоит только из цифр и имеет минимум 4 символа
    if not cleaned_number.isdigit():
        raise ValueError("Номер счёта должен содержать только цифры")
    if len(cleaned_number) < 4:
        raise ValueError("Номер счёта должен содержать минимум 4 цифры")

    # Возвращаем последние 4 цифры с ** в начале
    return f"**{cleaned_number[-4:]}"


print(get_mask_account(user_input))
