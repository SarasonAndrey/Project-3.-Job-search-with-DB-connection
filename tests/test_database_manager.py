import unittest
from unittest.mock import Mock, patch

import psycopg2

from src.database_manager import DBManager


class TestDBManager(unittest.TestCase):
    """Тесты для класса DBManager."""

    @patch("src.database_manager.psycopg2.connect")
    def test_init_and_get_companies(self, mock_connect):
        """Тест инициализации и получения компаний."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("Компания1", 10), ("Компания2", 5)]

        db_manager = DBManager("test_db", {"host": "localhost"})
        result = db_manager.get_companies_and_vacancies_count()

        expected = [
            {"company_name": "Компания1", "vacancies_count": 10},
            {"company_name": "Компания2", "vacancies_count": 5},
        ]
        self.assertEqual(result, expected)

    @patch("src.database_manager.psycopg2.connect")
    def test_get_all_vacancies(self, mock_connect):
        """Тест получения всех вакансий."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ("Компания1", "Вакансия1", 100000, "http://test1.com")
        ]

        db_manager = DBManager("test_db", {"host": "localhost"})
        result = db_manager.get_all_vacancies()

        expected = [
            {
                "company_name": "Компания1",
                "vacancy_name": "Вакансия1",
                "salary": 100000,
                "link": "http://test1.com",
            }
        ]
        self.assertEqual(result, expected)

    @patch("src.database_manager.psycopg2.connect")
    def test_init_connection_error(self, mock_connect):
        """Тест обработки ошибок подключения."""
        mock_connect.side_effect = psycopg2.Error("Connection error")

        with self.assertRaises(psycopg2.Error):
            DBManager("test_db", {"host": "localhost"})


if __name__ == "__main__":
    unittest.main()
