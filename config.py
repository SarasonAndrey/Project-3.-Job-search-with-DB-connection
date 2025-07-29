import os
from typing import Dict

from dotenv import load_dotenv


def config() -> Dict[str, str]:
    """Читает параметры подключения к базе данных из .env файла или переменных окружения."""
    load_dotenv()

    db: Dict[str, str] = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),
    }

    if not db["password"]:
        raise Exception(
            "Задайте переменные окружения: DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD"
        )

    return db
