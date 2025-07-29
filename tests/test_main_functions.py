import unittest
from unittest.mock import Mock, patch

from src.hh_api import get_vacancy_salary, search_vacancies_general


class TestMainFunctions(unittest.TestCase):
    """Тесты для основных функций проекта."""

    def test_get_vacancy_salary_edge_cases(self):
        """Тест граничных случаев извлечения зарплаты."""
        # Тест с неправильной валютой
        vacancy_wrong_currency = {
            "salary": {"from": 1000, "to": 2000, "currency": "USD"}
        }
        salary = get_vacancy_salary(vacancy_wrong_currency)
        self.assertIsNone(salary)

        # Тест только с from
        vacancy_from_only = {"salary": {"from": 100000, "currency": "RUR"}}
        salary = get_vacancy_salary(vacancy_from_only)
        self.assertEqual(salary, 100000)

    @patch("src.hh_api.requests.get")
    def test_search_vacancies_general(self, mock_get):
        """Тест поиска вакансий."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"name": "Test Vacancy"}]}
        mock_get.return_value = mock_response

        result = search_vacancies_general("Python")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Test Vacancy")


if __name__ == "__main__":
    unittest.main()
