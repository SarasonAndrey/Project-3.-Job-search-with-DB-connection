import psycopg2
from psycopg2 import sql


class DBManager:
    """
    Класс для управления подключением к базе данных PostgreSQL и выполнения запросов.

    Атрибуты:
        conn: Соединение с базой данных.
        cur: Курсор для выполнения запросов.

    Методы:
        get_companies_and_vacancies_count(): Получает список компаний и количество вакансий.
        get_all_vacancies(): Получает список всех вакансий с деталями.
        get_avg_salary(): Получает среднюю зарплату по вакансиям.
        get_vacancies_with_higher_salary(): Получает вакансии с зарплатой выше средней.
        get_vacancies_with_keyword(keyword): Получает вакансии по ключевому слову.
    """

    def __init__(self, dbname, params):
        try:
            self.conn = psycopg2.connect(dbname=dbname, **params)
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
            print("Успешно подключено к базе данных.")
        except psycopg2.Error as e:
            print(f"Ошибка подключения: {e}")
            raise

    def get_companies_and_vacancies_count(self):
        try:
            query = sql.SQL("""
                SELECT company_names, number_of_vacancies 
                FROM employers
            """)
            self.cur.execute(query)
            results = self.cur.fetchall()
            return [{'company_name': row[0], 'vacancies_count': row[1]} for row in results]
        except psycopg2.Error as e:
            print(f"Ошибка: {e}")
            return []

    def get_all_vacancies(self):
        try:
            query = sql.SQL("""
                SELECT e.company_names, v.vacancy_name, v.salary, v.link_to_the_vacancy 
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employers_id
            """)
            self.cur.execute(query)
            results = self.cur.fetchall()
            return [{'company_name': row[0], 'vacancy_name': row[1], 'salary': row[2], 'link': row[3]} for row in
                    results]
        except psycopg2.Error as e:
            print(f"Ошибка: {e}")
            return []

    def get_avg_salary(self):
        try:
            query = sql.SQL("""
                SELECT AVG(salary) 
                FROM vacancies
                WHERE salary IS NOT NULL  -- Игнорируем NULL значения
            """)
            self.cur.execute(query)
            result = self.cur.fetchone()[0]
            return result if result is not None else 0
        except psycopg2.Error as e:
            print(f"Ошибка: {e}")
            return 0

    def get_vacancies_with_higher_salary(self):
        try:
            avg_salary = self.get_avg_salary()
            query = sql.SQL("""
                SELECT e.company_names, v.vacancy_name, v.salary, v.link_to_the_vacancy 
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employers_id
                WHERE v.salary > %s
            """)
            self.cur.execute(query, (avg_salary,))
            results = self.cur.fetchall()
            return [{'company_name': row[0], 'vacancy_name': row[1], 'salary': row[2], 'link': row[3]} for row in
                    results]
        except psycopg2.Error as e:
            print(f"Ошибка: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword):
        try:
            query = sql.SQL("""
                SELECT e.company_names, v.vacancy_name, v.salary, v.link_to_the_vacancy 
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employers_id
                WHERE v.vacancy_name ILIKE %s
            """)
            search_pattern = f"%{keyword}%"
            self.cur.execute(query, (search_pattern,))
            results = self.cur.fetchall()
            return [{'company_name': row[0], 'vacancy_name': row[1], 'salary': row[2], 'link': row[3]} for row in
                    results]
        except psycopg2.Error as e:
            print(f"Ошибка: {e}")
            return []

    def __del__(self):
        if hasattr(self, 'cur') and self.cur:
            self.cur.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            print("Соединение закрыто.")
