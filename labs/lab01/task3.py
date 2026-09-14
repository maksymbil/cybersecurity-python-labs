"""Завдання 3: Хешування (sha3_224), CSV-база та JSON-логування."""

import csv
import hashlib
import json
import os
import sys
from collections.abc import Callable
from datetime import datetime, timezone
from functools import wraps

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import VARIANT_NUMBER

# Параметри Варіанта 2
MIN_PASSWORD_LENGTH = 10
PERSONAL_SALT = str(VARIANT_NUMBER).zfill(5)  # "00002"

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CSV_PATH = os.path.join(DATA_DIR, "users.csv")
LOG_PATH = os.path.join(DATA_DIR, "log.json")


class ValidationError(Exception):
    """Виняток для паролів, довжина яких менша за мінімальну за варіантом."""



def generate_hash(password: str, salt: str = "00000") -> str:
    """Генерує sha3_224 хеш конкатенації пароля та солі."""
    if not password or not salt:
        raise ValueError("Пароль та сіль не можуть бути порожніми.")

    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError(
            f"Пароль занадто короткий. Мінімум {MIN_PASSWORD_LENGTH} символів."
        )

    salted = (password + salt).encode("utf-8")
    return hashlib.sha3_224(salted).hexdigest()


def create_user(username: str, password: str) -> tuple[str, str]:
    """Створює запис користувача з розрахованим хешем."""
    hash_value = generate_hash(password, salt=PERSONAL_SALT)
    return (username, hash_value)


def create_users(users_list: list[tuple[str, str]]) -> None:
    """Записує користувачів у файл users.csv."""
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for username, password in users_list:
            u_login, u_hash = create_user(username, password)
            writer.writerow([u_login, u_hash])


def load_users_db() -> list[tuple[str, str]]:
    """Зчитує CSV-базу користувачів."""
    users_db: list[tuple[str, str]] = []

    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Файл бази даних {CSV_PATH} не знайдено.")

    with open(CSV_PATH, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                users_db.append((row[0], row[1]))

    return users_db


def log_event(func: Callable) -> Callable:
    """Декоратор аудиту: записує спроби автентифікації у log.json."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        username = args[0] if args else kwargs.get("username", "unknown")
        result = False

        try:
            result = func(*args, **kwargs)
        finally:
            log_entry = {
                "event": "login",
                "user": username,
                "result": "success" if result else "failure",
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "args": [],
                "kwargs": {},
            }

            try:
                os.makedirs(DATA_DIR, exist_ok=True)
                logs = []

                if os.path.exists(LOG_PATH):
                    try:
                        with open(LOG_PATH, mode="r", encoding="utf-8") as file:
                            logs = json.load(file)
                    except (OSError, json.JSONDecodeError):
                        logs = []

                logs.append(log_entry)

                with open(LOG_PATH, mode="w", encoding="utf-8") as file:
                    json.dump(
                        logs,
                        file,
                        indent=4,
                        ensure_ascii=False,
                    )
            except (OSError, FileNotFoundError, PermissionError):
                # Do not expose sensitive function arguments if logging fails.
                pass

        return result

    return wrapper


@log_event
def login(username: str, password: str, users_db: list[tuple[str, str]]) -> bool:
    """Звіряє введений логін і пароль із хешами в базі."""
    if not username or not password:
        raise ValueError("Логін і пароль є обов'язковими для заповнення.")

    try:
        input_hash = generate_hash(password, salt=PERSONAL_SALT)
    except ValidationError:
        return False

    for db_user, db_hash in users_db:
        if db_user == username and db_hash == input_hash:
            return True

    return False


def run_task3() -> None:
    """Демонстрація виконання кроків Завдання 3."""
    print("=" * 70)
    print(f"ЗАВДАННЯ 3: Хешування sha3_224, CSV та JSON (Варіант {VARIANT_NUMBER})")
    print("=" * 70)

    users_to_register = (
        ("admin_max", "AdminSuperPass2026!"),
        ("sec_officer", "ShieldDefender#99"),
        ("dev_john", "PythonCode@Works2"),
        ("qa_alice", "TestChecking2026$"),
        ("analyst_bob", "AuditMonitor!33"),
        ("cloud_dan", "ServerDeploy#77"),
        ("crypto_eva", "HashIntegrity@4"),
        ("support_kate", "HelpDeskTicket#55"),
        ("guest_visitor", "WelcomeGuestPass@1"),
        ("soc_lead", "IncidentHandler!10"),
    )

    try:
        # Реєстрація користувачів
        create_users(list(users_to_register))
        print("База users.csv успішно згенерована.")

        # Читання та відображення бази
        users_db = load_users_db()
        print("\nЗаписи у файлі users.csv:")
        print(f"{'Логін':<16} | {'Хеш (sha3_224)':<56}")
        print("-" * 75)
        for u_login, u_hash in users_db:
            print(f"{u_login:<16} | {u_hash}")

        # Тестування автентифікації та логування
        print("\nСпроби авторизації:")
        ok_login = login("admin_max", "AdminSuperPass2026!", users_db)
        print(f"Вхід admin_max (вірний пароль): {ok_login}")

        fail_login = login("admin_max", "WrongPassword123!", users_db)
        print(f"Вхід admin_max (невірний пароль): {fail_login}")

        unknown_login = login("unknown_user", "AnyValidPassword10!", users_db)
        print(f"Вхід невідомого користувача: {unknown_login}")

        print("\nЖурнал log.json оновлено.")

    except (OSError, FileNotFoundError, PermissionError) as file_err:
        print(f"[Помилка вводу/виводу файлів]: {file_err}")
    except ValidationError as val_err:
        print(f"[Помилка валідації пароля]: {val_err}")
    except ValueError as val_err:
        print(f"[Помилка аргументів]: {val_err}")
    print()


if __name__ == "__main__":
    run_task3()
