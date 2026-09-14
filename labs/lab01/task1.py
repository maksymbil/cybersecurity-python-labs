"""Завдання 1: Комплексний аналізатор надійності паролів."""

import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import VARIANT_NUMBER

# Вхідні дані Варіанта 2
PASSWORDS_INITIAL = [
    "Hello123!",
    "simple",
    "CompL3x@Pass",
    "password",
    "Str0ng#2023",
    "weak",
    "MySecur3!",
    "12345",
    "Advanced@1",
    "basic",
]

CRITERIA = {
    "min_length": 10,
    "require_digits": True,
    "require_upper": True,
    "require_special": True,
}

FORBIDDEN_PASSWORDS = {
    "password",
    "simple",
    "weak",
    "basic",
    "12345",
    "hello",
}


def prepare_passwords(passwords_list: list[str]) -> list[str]:
    """Генерує 3 випадкові дублікати та додає їх у кінець списку."""
    expanded_list = list(passwords_list)
    indices = random.sample(range(len(expanded_list)), 3)
    for idx in indices:
        expanded_list.append(expanded_list[idx])
    return expanded_list


def evaluate_password(password: str, full_list: list[str]) -> str:
    """Оцінює рівень стійкості окремого пароля за встановленими критеріями."""
    min_len = CRITERIA["min_length"]

    # Критерій: Заборонений
    if password.lower() in FORBIDDEN_PASSWORDS or len(password) < min_len:
        return "Заборонений"

    has_digit = any(c.isdigit() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_special = any(not c.isalnum() for c in password)

    all_criteria_met = has_digit and has_upper and has_special
    is_unique = full_list.count(password) == 1

    # Критерій: Дуже сильний
    if all_criteria_met and len(password) >= min_len + 4 and is_unique:
        return "Дуже сильний"

    # Критерій: Сильний
    if all_criteria_met:
        return "Сильний"

    # Критерій: Середній (довжина >= min_len і частина критеріїв виконана)
    if has_digit or has_upper or has_special:
        return "Середній"

    # Критерій: Слабкий
    return "Слабкий"


def run_task1() -> None:
    """Виконує аналіз списку паролів та виводить таблицю результатів."""
    print("=" * 70)
    print(f"ЗАВДАННЯ 1: Аналізатор надійності паролів (Варіант {VARIANT_NUMBER})")
    print("=" * 70)

    passwords = prepare_passwords(PASSWORDS_INITIAL)

    header = (
        f"{'№':<3} | {'Пароль':<18} | {'Довжина':<8} | {'Дублікат':<9} | {'Статус'}"
    )
    print(header)
    print("-" * len(header))

    for idx, pwd in enumerate(passwords, start=1):
        is_duplicate = "Так" if passwords.count(pwd) > 1 else "Ні"
        verdict = evaluate_password(pwd, passwords)
        print(f"{idx:<3} | {pwd:<18} | {len(pwd):<8} | {is_duplicate:<9} | {verdict}")
    print()


if __name__ == "__main__":
    run_task1()
