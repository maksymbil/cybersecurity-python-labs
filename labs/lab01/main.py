"""Головний модуль для демонстрації всієї лабораторної роботи №1."""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from labs.lab01.task1 import run_task1
from labs.lab01.task2 import run_task2
from labs.lab01.task3 import (
    PERSONAL_SALT,
    ValidationError,
    generate_hash,
    run_task3,
)
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER


def main() -> None:
    """Точка входу для демонстрації завдань."""
    print("=" * 70)
    print("НАЦІОНАЛЬНИЙ УНІВЕРСИТЕТ «ЛЬВІВСЬКА ПОЛІТЕХНІКА»")
    print("Звіт з виконання Лабораторної роботи №1")
    print(f"Студент: {STUDENT_NAME} | Група: {GROUP_NAME} | Варіант: {VARIANT_NUMBER}")
    print(f"Крипто-сіль: {PERSONAL_SALT} | Алгоритм: sha3_224")
    print("=" * 70)
    print()

    # Запуск Завдання 1
    run_task1()

    # Запуск Завдання 2
    run_task2()

    # Запуск Завдання 3
    run_task3()

    # Демонстрація генерації винятків
    print("=" * 70)
    print("ДЕМОНСТРАЦІЯ ОБРОБКИ ВИНЯТКІВ (Fail-Secure)")
    print("=" * 70)
    try:
        print("Спроба хешувати короткий пароль 'short':")
        generate_hash("short", salt=PERSONAL_SALT)
    except ValidationError as err:
        print(f"  -> Перехоплено ValidationError: {err}")

    try:
        print("Спроба хешувати порожній пароль '':")
        generate_hash("", salt=PERSONAL_SALT)
    except ValueError as err:
        print(f"  -> Перехоплено ValueError: {err}")
    print("=" * 70)


if __name__ == "__main__":
    main()
