"""Завдання 2: Багаторівнева система контролю доступу."""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import VARIANT_NUMBER

# Вхідні дані Варіанта 2
USERS = {
    "sysadmin02": {
        "role": "system_admin",
        "clearance": 4,
        "department": "Infrastructure",
        "active": True,
    },
    "analyst234": {
        "role": "security_analyst",
        "clearance": 3,
        "department": "SOC",
        "active": True,
    },
    "developer567": {
        "role": "developer",
        "clearance": 2,
        "department": "Development",
        "active": True,
    },
    "intern890": {
        "role": "intern",
        "clearance": 1,
        "department": "HR",
        "active": True,
    },
    "external123": {
        "role": "external",
        "clearance": 1,
        "department": "Vendor",
        "active": False,
    },
}

RESOURCES = [
    ("prod_database", 4),
    ("dev_environment", 2),
    ("documentation", 1),
    ("source_code", 3),
    ("server_configs", 4),
    ("test_data", 2),
    ("compliance_docs", 3),
    ("system_logs", 4),
    ("project_files", 2),
    ("public_wiki", 1),
]

SECURITY_LEVELS = ("Open", "Internal", "Restricted", "Top Secret")
BLOCKED_USERS = {"external123", "old_account", "test_user"}


def print_resources() -> None:
    """Виводить список доступних ресурсів із заміною чисел на назви грифів."""
    print("Каталог ресурсів системи:")
    for name, level in RESOURCES:
        text_level = SECURITY_LEVELS[level - 1]
        print(f"  * {name:<18} -> Рівень: {text_level} ({level})")
    print()


def check_access(username: str, resource_name: str, res_level: int) -> str:
    """Перевіряє права користувача до вказаного ресурсу."""
    if username not in USERS:
        return "DENY (User not found)"

    if username in BLOCKED_USERS:
        return "DENY (User is blocked)"

    user_data = USERS[username]
    if not user_data["active"]:
        return "DENY (Account inactive)"

    if user_data["clearance"] >= res_level:
        return "ALLOW"

    return "DENY (Insufficient clearance)"


def run_task2() -> None:
    """Запускає аудит доступу всіх облікових записів до ресурсів."""
    print("=" * 70)
    print(f"ЗАВДАННЯ 2: Система контролю доступу (Варіант {VARIANT_NUMBER})")
    print("=" * 70)

    print_resources()

    print("Журнал аудиту запитів доступу:")
    for username in USERS:
        for res_name, res_level in RESOURCES:
            decision = check_access(username, res_name, res_level)
            print(f"user=[{username}] resource=[{res_name}] -> {decision}")
    print()


if __name__ == "__main__":
    run_task2()
