import psycopg2
from psycopg2 import sql


def create_database_and_tables(dbname, params, force_recreate=False):
    """Создает базу данных PostgreSQL и таблицы."""
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(dbname="postgres", **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
        if not cur.fetchone():
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=dbname, **params)
        conn.autocommit = True
        cur = conn.cursor()

        if force_recreate:
            cur.execute("DROP TABLE IF EXISTS vacancies, employers;")

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS employers (
                employers_id SERIAL PRIMARY KEY,
                company_names VARCHAR NOT NULL,
                number_of_vacancies INTEGER
            )
        """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR NOT NULL,
                salary INTEGER,
                link_to_the_vacancy TEXT,
                employer_id INTEGER REFERENCES employers(employers_id)
            )
        """
        )

    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def insert_employer_data(conn, company_name, vacancy_count):
    """Вставляет данные о работодателе."""
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO employers (company_names, number_of_vacancies)
            VALUES (%s, %s)
            RETURNING employers_id
        """,
            (company_name, vacancy_count),
        )

        employer_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return employer_id
    except psycopg2.Error as e:
        print(f"Ошибка при вставке данных работодателя '{company_name}': {e}")
        conn.rollback()
        return None


def insert_vacancy_data(conn, vacancy_name, salary, link, employer_id):
    """Вставляет данные о вакансии."""
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO vacancies (vacancy_name, salary, link_to_the_vacancy, employer_id)
            VALUES (%s, %s, %s, %s)
        """,
            (vacancy_name[:500], salary, link, employer_id),
        )
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print(f"Ошибка при вставке вакансии: {e}")
        conn.rollback()
