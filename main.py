import time

import psycopg2

from config import config
from src.database_manager import DBManager
from src.database_setup import (
    create_database_and_tables,
    insert_employer_data,
    insert_vacancy_data,
)
from src.hh_api import (
    get_known_employers,
    get_vacancies_by_employer,
    get_vacancy_salary,
    search_vacancies_general,
)


def load_data_to_database():
    """Загружает данные о компаниях и вакансиях в базу данных."""
    params = config()

    try:
        conn = psycopg2.connect(dbname="hh", **params)
        conn.autocommit = False
        known_employers = get_known_employers()

        total_vacancies_inserted = 0

        for company_name, employer_id in known_employers.items():
            print(f"Обрабатываю компанию: {company_name} (ID: {employer_id})")

            vacancies = get_vacancies_by_employer(employer_id, per_page=30)
            print(f"Найдено вакансий: {len(vacancies)}")

            if vacancies:
                employer_db_id = insert_employer_data(
                    conn, company_name, len(vacancies)
                )

                if employer_db_id:
                    inserted_count = 0
                    for vacancy in vacancies[:20]:
                        vacancy_name = vacancy.get("name", "Не указано")
                        salary = get_vacancy_salary(vacancy)
                        link = vacancy.get("alternate_url", "")

                        insert_vacancy_data(
                            conn, vacancy_name, salary, link, employer_db_id
                        )
                        inserted_count += 1
                        total_vacancies_inserted += 1

                    print(f"Вставлено {inserted_count} вакансий для {company_name}")
                    conn.commit()
            else:
                print(f"Не найдено вакансий для компании: {company_name}")

        print("\nИщу дополнительные вакансии по ключевым словам...")
        search_terms = ["Python", "Java", "JavaScript", "Data Scientist"]

        for term in search_terms:
            print(f"Ищу вакансии по запросу: {term}")
            vacancies = search_vacancies_general(term, per_page=20)
            print(f"Найдено вакансий: {len(vacancies)}")

            if vacancies:
                employer_db_id = insert_employer_data(
                    conn, f"Поиск_{term}", len(vacancies)
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

                    print(f"Вставлено {inserted_count} вакансий для поиска '{term}'")
                    conn.commit()

        conn.close()
        print(
            f"\nДанные успешно загружены в базу данных. Всего вставлено вакансий: {total_vacancies_inserted}"
        )

    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        import traceback

        traceback.print_exc()


def display_results():
    """Отображает результаты из базы данных."""
    params = config()

    try:
        db_manager = DBManager("hh", params)

        print("\n" + "=" * 50)
        print("КОМПАНИИ И КОЛИЧЕСТВО ВАКАНСИЙ")
        print("=" * 50)
        companies = db_manager.get_companies_and_vacancies_count()
        if companies:
            for company in companies:
                print(
                    f"{company['company_name']}: {company['vacancies_count']} вакансий"
                )
        else:
            print("Нет данных о компаниях")

        print("\n" + "=" * 50)
        print("ВСЕ ВАКАНСИИ")
        print("=" * 50)
        vacancies = db_manager.get_all_vacancies()
        if vacancies:
            for i, vacancy in enumerate(vacancies[:20], 1):
                salary_str = (
                    f"Зарплата: {vacancy['salary']}"
                    if vacancy["salary"]
                    else "Зарплата: не указана"
                )
                print(
                    f"{i}. {vacancy['company_name']} - {vacancy['vacancy_name']} - {salary_str}"
                )
        else:
            print("Нет данных о вакансиях")

        print("\n" + "=" * 50)
        print("СРЕДНЯЯ ЗАРПЛАТА")
        print("=" * 50)
        avg_salary = db_manager.get_avg_salary()
        if avg_salary > 0:
            print(f"Средняя зарплата: {avg_salary:.2f} руб.")
        else:
            print("Нет данных для расчета средней зарплаты")

        if avg_salary > 0:
            print("\n" + "=" * 50)
            print(f"ВАКАНСИИ С ЗАРПЛАТОЙ ВЫШЕ СРЕДНЕЙ ({avg_salary:.2f} руб.)")
            print("=" * 50)
            high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            if high_salary_vacancies:
                for i, vacancy in enumerate(high_salary_vacancies[:15], 1):
                    print(
                        f"{i}. {vacancy['company_name']} - {vacancy['vacancy_name']} - "
                        f"Зарплата: {vacancy['salary']} руб."
                    )
            else:
                print("Нет вакансий с зарплатой выше средней")

        keyword = "Python"
        print("\n" + "=" * 50)
        print(f"ВАКАНСИИ С КЛЮЧЕВЫМ СЛОВОМ '{keyword}'")
        print("=" * 50)
        keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
        if keyword_vacancies:
            for i, vacancy in enumerate(keyword_vacancies[:15], 1):
                salary_str = (
                    f"Зарплата: {vacancy['salary']}"
                    if vacancy["salary"]
                    else "Зарплата: не указана"
                )
                print(
                    f"{i}. {vacancy['company_name']} - {vacancy['vacancy_name']} - {salary_str}"
                )
        else:
            print(f"Нет вакансий с ключевым словом '{keyword}'")

        db_manager.close_connection()

    except Exception as e:
        print(f"Ошибка при отображении результатов: {e}")
        import traceback

        traceback.print_exc()


def main():
    """Основная функция программы."""
    params = config()
    create_database_and_tables("hh", params, force_recreate=True)

    load_data_to_database()

    time.sleep(2)

    display_results()


if __name__ == "__main__":
    main()
