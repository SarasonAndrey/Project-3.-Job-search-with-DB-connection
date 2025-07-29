import os
import shutil
import tempfile
import unittest

from src.file_handler import load_data_from_json, save_data_to_json


class TestFileHandler(unittest.TestCase):
    """Тесты для модуля работы с файлами."""

    def setUp(self):
        """Подготовка перед каждым тестом."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_data.json")
        self.test_data = {"test": "data", "number": 42}

    def tearDown(self):
        """Очистка после каждого теста."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_save_and_load_data(self):
        """Тест сохранения и загрузки данных."""
        result = save_data_to_json(self.test_data, self.test_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_file))

        loaded_data = load_data_from_json(self.test_file)
        self.assertEqual(loaded_data, self.test_data)

    def test_load_nonexistent_file(self):
        """Тест загрузки несуществующего файла."""
        nonexistent_file = os.path.join(self.test_dir, "nonexistent.json")
        loaded_data = load_data_from_json(nonexistent_file)
        self.assertIsNone(loaded_data)


if __name__ == "__main__":
    unittest.main()
