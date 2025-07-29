import unittest
from unittest.mock import Mock, patch

from config import config


class TestConfig(unittest.TestCase):
    """Тесты для модуля конфигурации."""

    @patch("config.ConfigParser")
    def test_config_success(self, mock_config_parser):
        """Тест успешного чтения конфигурации."""
        mock_parser = Mock()
        mock_config_parser.return_value = mock_parser
        mock_parser.has_section.return_value = True
        mock_parser.items.return_value = [
            ("host", "localhost"),
            ("database", "test_db"),
        ]

        result = config()
        expected = {"host": "localhost", "database": "test_db"}
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
