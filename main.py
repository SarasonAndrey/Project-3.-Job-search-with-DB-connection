import os

import psycopg2

from config import config
from src.database_manager import DBManager
from src.database_setup import (create_database_and_tables,
                                insert_employer_data, insert_vacancy_data)
from src.file_handler import save_data_to_json
from src.hh_api import (get_known_employers, get_vacancies_by_employer,
                        get_vacancy_salary, search_vacancies_general)


def collect_and_save_raw_data():
    """Собирает и сохраняет сырые данные для отладки."""
    os.makedirs("data", exist_ok=True)

    # Сохраняем список известных работодателей
    employers = get_known_employers()
    save_data_to_json(employers, "data/known_employers.json")

    # Собираем примеры данных
    sample_data = {}

    # Пример данных для одного работодателя
    if employers:
        first_employer_name = list(employers.keys())[0]
        first_employer_id = employers[first_employer_name]
        sample_vacancies = get_vacancies_by_employer(first_employer_id, per_page=5)
        sample_data["sample_employer_vacancies"] = {
            "employer": first_employer_name,
            "vacancies": sample_vacancies,
        }

    # Пример поиска
    sample_search = search_vacancies_general("Python", per_page=5)
    sample_data["sample_search_results"] = sample_search

    save_data_to_json(sample_data, "data/sample_data.json")


def load_data_to_database():
    """Загружает данные о компаниях и вакансиях в базу данных."""
    params = config()

    try:
        conn = psycopg2.connect(dbname="hh", **params)
        conn.autocommit = False
        known_employers = get_known_employers()

        total_employers = 0
        total_vacancies_inserted = 0

        print("Загружаю данные для известных работодателей...")

        for company_name, employer_id in known_employers.items():
            print(f"Обрабатываю компанию: {company_name}")

            vacancies = get_vacancies_by_employer(employer_id, per_page=25)
            print(f"Найдено вакансий: {len(vacancies)}")

            if vacancies:
                employer_db_id = insert_employer_data(
                    conn, company_name, len(vacancies)
                )

                if employer_db_id:
                    inserted_count = 0
                    for vacancy in vacancies[:15]:
                        vacancy_name = vacancy.get("name", "Не указано")
                        salary = get_vacancy_salary(vacancy)
                        link = vacancy.get("alternate_url", "")

                        insert_vacancy_data(
                            conn, vacancy_name, salary, link, employer_db_id
                        )
                        inserted_count += 1
                        total_vacancies_inserted += 1

                    print(f"Вставлено {inserted_count} вакансий")
                    conn.commit()
                    total_employers += 1

        print(f"\nЗагружено данных для {total_employers} компаний")
        print(f"Всего вставлено вакансий: {total_vacancies_inserted}")
        conn.close()

        # Сохраняем статистику загрузки
        stats = {
            "total_employers_processed": total_employers,
            "total_vacancies_inserted": total_vacancies_inserted,
        }
        save_data_to_json(stats, "data/load_statistics.json")

    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")


def display_results():
    """Отображает результаты из базы данных."""
    params = config()

    try:
        db_manager = DBManager("hh", params)

        # Компании и количество вакансий
        print("\n=== Компании и количество вакансий ===")
        companies = db_manager.get_companies_and_vacancies_count()
        if companies:
            for company in companies:
                print(
                    f"{company['company_name']}: {company['vacancies_count']} вакансий"
                )
        else:
            print("Нет данных")

        # Все вакансии
        print("\n=== Все вакансии ===")
        vacancies = db_manager.get_all_vacancies()
        if vacancies:
            for i, vacancy in enumerate(vacancies[:15], 1):
                salary_info = (
                    f"Зарплата: {vacancy['salary']}"
                    if vacancy["salary"]
                    else "Зарплата: не указана"
                )
                print(
                    f"{i}. {vacancy['company_name']} - {vacancy['vacancy_name']} - {salary_info}"
                )
        else:
            print("Нет данных")

        # Средняя зарплата
        print("\n=== Средняя зарплата ===")
        avg_salary = db_manager.get_avg_salary()
        if avg_salary > 0:
            print(f"Средняя зарплата: {avg_salary:.2f} руб.")
        else:
            print("Нет данных для расчета")

        # Вакансии с высокой зарплатой
        if avg_salary > 0:
            print(
                f"\n=== Вакансии с зарплатой выше средней ({avg_salary:.2f} руб.) ==="
            )
            high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            if high_salary_vacancies:
                for i, vacancy in enumerate(high_salary_vacancies[:10], 1):
                    print(
                        f"{i}. {vacancy['company_name']} - {vacancy['vacancy_name']} - {vacancy['salary']} руб."
                    )
            else:
                print("Нет вакансий")

        # Поиск по ключевому слову
        keyword = "Python"
        print(f"\n=== Вакансии с ключевым словом '{keyword}' ===")
        keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
        if keyword_vacancies:
            for i, vacancy in enumerate(keyword_vacancies[:10], 1):
                salary_info = (
                    f"Зарплата: {vacancy['salary']}"
                    if vacancy["salary"]
                    else "Зарплата: не указана"
                )
                print(
                    f"{i}. {vacancy['company_name']} - {vacancy['vacancy_name']} - {salary_info}"
                )
        else:
            print(f"Нет вакансий с ключевым словом '{keyword}'")

        # Сохраняем результаты в файл
        results = {
            "companies": companies,
            "all_vacancies_count": len(vacancies) if vacancies else 0,
            "avg_salary": avg_salary,
            "high_salary_vacancies_count": (
                len(high_salary_vacancies) if "high_salary_vacancies" in locals() else 0
            ),
            "keyword_vacancies_count": (
                len(keyword_vacancies) if keyword_vacancies else 0
            ),
        }
        save_data_to_json(results, "data/query_results.json")

    except Exception as e:
        print(f"Ошибка при отображении результатов: {e}")


def main():
    """Основная функция программы."""
    print("Создаю базу данных и таблицы...")
    params = config()
    create_database_and_tables("hh", params, force_recreate=True)

    print("Собираю и сохраняю сырые данные...")
    collect_and_save_raw_data()

    print("Загружаю данные...")
    load_data_to_database()

    print("Отображаю результаты...")
    display_results()

    print("\nРабота с файлами:")
    print("- Сырые данные сохранены в папке 'data'")
    print("- Результаты запросов сохранены в 'data/query_results.json'")
    print("- Статистика загрузки в 'data/load_statistics.json'")


if __name__ == "__main__":
    main()
