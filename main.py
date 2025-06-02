from pprint import pprint

from config import config
from src.connect_database import create_database_and_tables

from src.data_employers_vacancies import fetch_emploers_vaconcies, save_data_to_file
from src.list_vacancies_companies import DBManager

file_path = "C:\\Users\\YOGA 260\\Pycharm_MY_Projects\\Курсовые\\project3_1\\data.json"
BASE_URL = "https://api.hh.ru/vacancies"
# BASE_URL = "https://pokeapi.co/api/v2/pokemon?limit=10"
params = config()
interesting_companies = [
    "Studio Nargiz balloons&Flowers"
]
db_manager = DBManager('hh', params)


def main():
    data_hh = (fetch_emploers_vaconcies(BASE_URL))
    pprint(data_hh)
    create_database_and_tables('hh', params, force_recreate=True)
    save_data_to_file(data_hh, file_path)

    db_manager = DBManager('hh', params)


companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
print("Список компаний и количество вакансий:")
for item in companies_and_vacancies:
    print(f"Компания: {item['company_name']}, Вакансий: {item['vacancies_count']}")

# 2. Получить список всех вакансий
all_vacancies = db_manager.get_all_vacancies()
print("\nСписок всех вакансий:")
for vacancy in all_vacancies:
    print(f"Компания: {vacancy['company_name']}, Вакансия: {vacancy['vacancy_name']}, "
          f"Зарплата: {vacancy['salary']}, Ссылка: {vacancy['link']}")

# 3. Получить среднюю зарплату
avg_salary = db_manager.get_avg_salary()
print(f"\nСредняя зарплата по вакансиям: {avg_salary}")

# 4. Получить вакансии с зарплатой выше средней
higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
print("\nВакансии с зарплатой выше средней:")
for vacancy in higher_salary_vacancies:
    print(f"Компания: {vacancy['company_name']}, Вакансия: {vacancy['vacancy_name']}, "
          f"Зарплата: {vacancy['salary']}, Ссылка: {vacancy['link']}")

# 5. Получить вакансии по ключевому слову
keyword = "Python"
keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
print(f"\nВакансии, содержащие ключевое слово '{keyword}':")
for vacancy in keyword_vacancies:
    print(f"Компания: {vacancy['company_name']}, Вакансия: {vacancy['vacancy_name']}, "
          f"Зарплата: {vacancy['salary']}, Ссылка: {vacancy['link']}")

if __name__ == "__main__":
    main()  # Запускаем основную функцию
