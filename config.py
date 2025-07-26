from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    """Читает параметры подключения к базе данных."""
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        params = parser.items(section)
        db = {param[0]: param[1] for param in params}
    else:
        raise Exception(f"Секция '{section}' не найдена в файле '{filename}'.")

    return db
