import json
from src.library_catalog.models import BaseBook
from src.api.open_library_api import OpenLibraryAPI
from src.logger.logger import setup_logger

logger = setup_logger("service.func")



def open_library_book(title: str):
    """ Сервисная функция для запроса книги из сервиса OpenLibrary"""

    logger.info("Работа функции запроса книги из сервиса OpenLibrary ")
    api = OpenLibraryAPI()
    try:
        book = api.search(title)
        if book:
            return book
        elif title == "string":
            return "Книга не найдена"

    finally:
        api.close()


def open_library_description(func: open_library_book):
    """ Сервисная функция для определения описания найденной книги """

    logger.info("Работа функции для определения описания найденной книги ")
    api = OpenLibraryAPI()
    work_key = func.get("key")
    if work_key:
        details = api.get_book_details(work_key)
        return details["description"]["value"]
    else:
        return None


def open_library_rating(func: open_library_book):
    """ Сервисная функция для определения рейтинга найденной книги """

    logger.info("Работа функции для определения рейтинга найденной книги ")
    api = OpenLibraryAPI()
    work_key = func.get("key")
    if work_key:
        rating_api = api.get_rating(work_key)
        return round(float(rating_api), 1)
    else:
        return None


def open_library_cover(func: open_library_book):
    """ Сервисная функция для получения ссылки на обложку найденной книги"""

    logger.info("Работа функции для получения ссылки на обложку найденной книги ")
    api = OpenLibraryAPI()
    cover_id = func.get("cover_i")
    if cover_id:
        cover_url = api.get_cover_url(cover_id)
        return cover_url
    else:
        return None


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
