from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    """
    Читает параметры подключения к базе данных из файла database.ini.

    Аргументы:
        filename (str): Имя конфигурационного файла.
        section (str): Секция в файле, содержащая параметры подключения.

    Возвращает:
        dict: Словарь с параметрами подключения.
    """
    # Создаем объект парсера
    parser = ConfigParser()

    # Читаем конфигурационный файл
    parser.read(filename)

    # Проверяем, существует ли указанная секция
    if parser.has_section(section):
        params = parser.items(section)  # Получаем все параметры секции
        db = {param[0]: param[1] for param in params}  # Преобразуем в словарь

    else:
        raise Exception(f"Секция '{section}' не найдена в файле '{filename}'.")
    return db
