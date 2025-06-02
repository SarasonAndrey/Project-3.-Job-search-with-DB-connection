import json

import requests


def fetch_emploers_vaconcies(BASE_URL):
    if not isinstance(BASE_URL, str):
        print(f"Ошибка: BASE_URL должен быть строкой")
        return None
    try:
        BASE_URL = BASE_URL.strip()
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Ошибка подключения: код {response.status_code}")
            return None
    except ValueError:
        print("Ошибка: Ответ сервера не является валидным Json")
        return None


def save_data_to_file(data, file_path):
    """
    Функция сохраняет данные в файл в формате JSON.

    Аргументы:
        data (dict): Данные для сохранения.
        file_path (str): Путь к файлу, куда будут сохранены данные.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)  # Записываем данные в файл
        print(f"Данные успешно сохранены в файл: {file_path}")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")
