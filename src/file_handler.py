import json
import os
from typing import Any, Optional


def save_data_to_json(data: Any, file_path: str) -> bool:
    """Сохраняет данные в JSON файл."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении данных в файл: {e}")
        return False


def load_data_from_json(file_path: str) -> Optional[Any]:
    """Загружает данные из JSON файла."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return None
    except Exception as e:
        print(f"Ошибка при загрузке данных из файла: {e}")
        return None


def save_vacancies_to_file(
    vacancies_data: Any, filename: str = "vacancies_data.json"
) -> bool:
    """Сохраняет данные о вакансиях в файл."""
    file_path = os.path.join("data", filename)
    return save_data_to_json(vacancies_data, file_path)


def load_vacancies_from_file(filename: str = "vacancies_data.json") -> Optional[Any]:
    """Загружает данные о вакансиях из файла."""
    file_path = os.path.join("data", filename)
    return load_data_from_json(file_path)
