import unittest
from unittest.mock import Mock, patch

from src.database_setup import (create_database_and_tables,
                                insert_employer_data, insert_vacancy_data)


class TestDatabaseSetup(unittest.TestCase):
    """Тесты для модуля настройки базы данных."""

    def test_insert_employer_data_success(self):
        """Тест успешной вставки данных работодателя."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]

        result = insert_employer_data(mock_conn, "Тестовая компания", 10)
        self.assertEqual(result, 1)

    def test_insert_vacancy_data_no_exceptions(self):
        """Тест вставки данных вакансии без исключений."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor

        try:
            insert_vacancy_data(
                mock_conn, "Тестовая вакансия", 100000, "http://test.com", 1
            )
            success = True
        except Exception:
            success = False

        self.assertTrue(success)

    @patch("src.database_setup.psycopg2.connect")
    def test_create_database_and_tables(self, mock_connect):
        """Тест создания базы данных и таблиц."""
        mock_conn1 = Mock()
        mock_conn2 = Mock()
        mock_cursor1 = Mock()
        mock_cursor2 = Mock()

        mock_connect.side_effect = [mock_conn1, mock_conn2]
        mock_conn1.cursor.return_value = mock_cursor1
        mock_conn2.cursor.return_value = mock_cursor2
        mock_cursor1.fetchone.return_value = None  # База не существует

        try:
            create_database_and_tables("test_db", {"host": "localhost"})
            success = True
        except Exception:
            success = False

        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
