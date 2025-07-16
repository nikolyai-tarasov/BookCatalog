import json
from src.library_catalog.app.catalog.models import BaseBook
from src.library_catalog.app.logger.logger import setup_logger

logger = setup_logger("service_file.func")


def open_file_r(file_path):
    """ Сервисная функция для чтения файла JSON"""

    logger.info("Работа функции для чтения файла JSON ")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    except FileNotFoundError:
        return "Файл не найден"

    except Exception as e:
        print(f"Другая ошибка{e}")


def open_file_w(file_path, book: BaseBook):
    """ Сервисная функция для записи в JSON файл """

    logger.info("Работа функции для записи в JSON файл ")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(book, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing to JSON file: {e}")
