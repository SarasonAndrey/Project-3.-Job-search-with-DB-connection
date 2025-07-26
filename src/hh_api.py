import requests


def get_known_employers():
    """Возвращает словарь известных работодателей с их ID."""
    return {
        "Яндекс": "1740",
        "Сбер": "3529",
        "Тинькофф": "78638",
        "VK": "3420",
        "Ozon": "2108",
        "Wildberries": "4236",
        "Авито": "8458",
        "HeadHunter": "1455",
        "Mail.ru": "3291",
        "Rambler": "2337",
    }


def get_vacancies_by_employer(employer_id, per_page=50):
    """Получает вакансии по ID работодателя."""
    try:
        url = "https://api.hh.ru/vacancies"
        params = {"employer_id": employer_id, "per_page": min(per_page, 100), "page": 0}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data["items"]
        else:
            print(f"HTTP ошибка {response.status_code} для работодателя {employer_id}")
        return []
    except Exception as e:
        print(f"Ошибка при получении вакансий: {e}")
        return []


def get_vacancy_salary(vacancy):
    """Извлекает зарплату из вакансии."""
    salary = vacancy.get("salary")
    if salary and salary.get("currency") in ["RUR", "RUB"]:
        if salary.get("from") and salary.get("to"):
            return (salary["from"] + salary["to"]) // 2
        elif salary.get("from"):
            return salary["from"]
        elif salary.get("to"):
            return salary["to"]
    return None


def search_vacancies_general(search_text, area="113", per_page=30):
    """Поиск вакансий по общему тексту."""
    try:
        url = "https://api.hh.ru/vacancies"
        params = {
            "text": search_text,
            "area": area,
            "per_page": min(per_page, 100),
            "page": 0,
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data["items"]
        return []
    except Exception as e:
        print(f"Ошибка при поиске вакансий: {e}")
        return []
