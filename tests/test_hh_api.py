import unittest

from src.hh_api import get_known_employers, get_vacancy_salary


class TestHhApi(unittest.TestCase):
    """Тесты для модуля работы с API hh.ru."""

    def test_get_known_employers(self):
        """Тест получения известных работодателей."""
        employers = get_known_employers()
        self.assertIsInstance(employers, dict)
        self.assertGreater(len(employers), 0)
        self.assertIn("Яндекс", employers)

    def test_get_vacancy_salary(self):
        """Тест извлечения зарплаты."""
        vacancy = {"salary": {"from": 100000, "to": 150000, "currency": "RUR"}}
        salary = get_vacancy_salary(vacancy)
        self.assertEqual(salary, 125000)

        vacancy_no_salary = {"name": "Test vacancy"}
        salary_none = get_vacancy_salary(vacancy_no_salary)
        self.assertIsNone(salary_none)


if __name__ == "__main__":
    unittest.main()
