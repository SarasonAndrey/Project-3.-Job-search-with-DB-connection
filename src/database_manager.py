from typing import Any, Dict, List, Optional, Union

import psycopg2


class DBManager:
    """Класс для управления подключением к базе данных PostgreSQL."""

    def __init__(self, dbname: str, params: Dict[str, str]) -> None:
        """Инициализирует подключение к базе данных."""
        self.dbname: str = dbname
        self.params: Dict[str, str] = params
        self.conn: Optional[Any] = None
        self.cur: Optional[Any] = None
        self._connect()

    def _connect(self) -> None:
        """Устанавливает соединение с базой данных."""
        if self.conn:
            self.close_connection()
        self.conn = psycopg2.connect(dbname=self.dbname, **self.params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> List[Dict[str, Union[str, int]]]:
        """Получает список всех компаний и количество вакансий."""
        try:
            self._connect()
            query = """
                SELECT company_names, number_of_vacancies
                FROM employers
                ORDER BY number_of_vacancies DESC
            """
            self.cur.execute(query)
            results = self.cur.fetchall()
            self.cur.close()
            return [
                {"company_name": row[0], "vacancies_count": row[1]} for row in results
            ]
        except psycopg2.Error as e:
            print(f"Ошибка при получении компаний: {e}")
            return []

    def get_all_vacancies(self) -> List[Dict[str, Union[str, int, None]]]:
        """Получает список всех вакансий."""
        try:
            self._connect()
            query = """
                SELECT e.company_names, v.vacancy_name, v.salary, v.link_to_the_vacancy
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employers_id
                ORDER BY e.company_names, v.salary DESC NULLS LAST
            """
            self.cur.execute(query)
            results = self.cur.fetchall()
            self.cur.close()
            return [
                {
                    "company_name": row[0],
                    "vacancy_name": row[1],
                    "salary": row[2],
                    "link": row[3],
                }
                for row in results
            ]
        except psycopg2.Error as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям."""
        try:
            self._connect()
            query = """
                SELECT AVG(salary)
                FROM vacancies
                WHERE salary IS NOT NULL
            """
            self.cur.execute(query)
            result = self.cur.fetchone()[0]
            self.cur.close()
            return result if result is not None else 0
        except psycopg2.Error as e:
            print(f"Ошибка при получении средней зарплаты: {e}")
            return 0

    def get_vacancies_with_higher_salary(
        self,
    ) -> List[Dict[str, Union[str, int, None]]]:
        """Получает вакансии с зарплатой выше средней."""
        try:
            self._connect()
            avg_salary = self.get_avg_salary()
            query = """
                SELECT e.company_names, v.vacancy_name, v.salary, v.link_to_the_vacancy
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employers_id
                WHERE v.salary > %s
                ORDER BY v.salary DESC
            """
            self.cur.execute(query, (avg_salary,))
            results = self.cur.fetchall()
            self.cur.close()
            return [
                {
                    "company_name": row[0],
                    "vacancy_name": row[1],
                    "salary": row[2],
                    "link": row[3],
                }
                for row in results
            ]
        except psycopg2.Error as e:
            print(f"Ошибка при получении вакансий с высокой зарплатой: {e}")
            return []

    def get_vacancies_with_keyword(
        self, keyword: str
    ) -> List[Dict[str, Union[str, int, None]]]:
        """Получает вакансии по ключевому слову."""
        try:
            self._connect()
            query = """
                SELECT e.company_names, v.vacancy_name, v.salary, v.link_to_the_vacancy
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employers_id
                WHERE v.vacancy_name ILIKE %s
                ORDER BY v.salary DESC NULLS LAST
            """
            search_pattern = f"%{keyword}%"
            self.cur.execute(query, (search_pattern,))
            results = self.cur.fetchall()
            self.cur.close()
            return [
                {
                    "company_name": row[0],
                    "vacancy_name": row[1],
                    "salary": row[2],
                    "link": row[3],
                }
                for row in results
            ]
        except psycopg2.Error as e:
            print(f"Ошибка при поиске вакансий по ключевому слову: {e}")
            return []

    def close_connection(self) -> None:
        """Закрывает соединение с базе данных."""
        if hasattr(self, "cur") and self.cur:
            self.cur.close()
        if hasattr(self, "conn") and self.conn:
            self.conn.close()

    def __del__(self) -> None:
        """Деструктор класса."""
        self.close_connection()
