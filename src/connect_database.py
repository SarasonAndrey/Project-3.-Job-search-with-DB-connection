import psycopg2
from psycopg2 import sql


def create_database_and_tables(dbname, params, force_recreate=False):
    """
    Создает базу данных PostgreSQL, если она не существует, и таблицы 'employers' и 'vacancies' внутри неё.
    Если force_recreate=True, удалит и пересоздаст таблицы, если они существуют (это удалит данные!).

    Аргументы:
        dbname (str): Имя создаваемой базы данных.
        params (dict): Параметры подключения к PostgreSQL (например, host, user, password).
        force_recreate (bool): Если True, удалит и пересоздаст таблицы 'employers' и 'vacancies'.
    """
    conn = None
    cur = None

    try:
        # Подключаемся к 'postgres' для создания базы
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        # Проверяем и создаем базу данных
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
        if not cur.fetchone():
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))

        cur.close()
        conn.close()

        # Подключаемся к целевой базе
        conn = psycopg2.connect(dbname=dbname, **params)
        conn.autocommit = True
        cur = conn.cursor()

        # Проверяем и создаем таблицу 'employers'
        cur.execute("SELECT 1 FROM information_schema.tables WHERE table_name = %s;", ('employers',))
        if not cur.fetchone() or force_recreate:
            if force_recreate:
                cur.execute("DROP TABLE IF EXISTS employers;")
            cur.execute(
                sql.SQL("""
                    CREATE TABLE {} (
                        employers_id SERIAL PRIMARY KEY,
                        company_names VARCHAR NOT NULL,
                        number_of_vacancies INTEGER
                    )
                """).format(sql.Identifier('employers'))
            )

        # Проверяем и создаем таблицу 'vacancies'
        cur.execute("SELECT 1 FROM information_schema.tables WHERE table_name = %s;", ('vacancies',))
        if not cur.fetchone() or force_recreate:
            if force_recreate:
                cur.execute("DROP TABLE IF EXISTS vacancies;")
            cur.execute(
                sql.SQL("""
                    CREATE TABLE {} (
                        vacancies_id SERIAL PRIMARY KEY,
                        vacancy_name VARCHAR NOT NULL,
                        salary INTEGER,
                        link_to_the_vacancy VARCHAR,
                        employer_id INTEGER  -- Ссылка на employers, если нужно
                    )
                """).format(sql.Identifier('vacancies'))
            )

    except psycopg2.Error as e:
        raise  # Передаем ошибку дальше
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



