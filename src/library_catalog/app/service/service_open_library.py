from fastapi.params import Depends
from src.library_catalog.app.api.open_library_api import OpenLibraryAPI
from src.library_catalog.app.logger.logger import setup_logger

logger = setup_logger("service_open_library.func")


def open_library_book(title: str, api: OpenLibraryAPI = Depends(OpenLibraryAPI)):
    """ Сервисная функция для запроса книги из сервиса OpenLibrary"""

    logger.info("Работа функции запроса книги из сервиса OpenLibrary ")

    try:
        book = api.search(title)
        if book:
            return book
        elif title == "string":
            return "Книга не найдена"

    finally:
        api.close()


def open_library_description(func: open_library_book, api: OpenLibraryAPI = Depends(OpenLibraryAPI)):
    """ Сервисная функция для определения описания найденной книги """

    logger.info("Работа функции для определения описания найденной книги ")
    work_key = func.get("key")
    if work_key:
        details = api.get_book_details(work_key)
        return details["description"]["value"]
    else:
        return None


def open_library_rating(func: open_library_book, api: OpenLibraryAPI = Depends(OpenLibraryAPI)):
    """ Сервисная функция для определения рейтинга найденной книги """

    logger.info("Работа функции для определения рейтинга найденной книги ")
    work_key = func.get("key")
    if work_key:
        rating_api = api.get_rating(work_key)
        return round(float(rating_api), 1)
    else:
        return None


def open_library_cover(func: open_library_book, api: OpenLibraryAPI = Depends(OpenLibraryAPI)):
    """ Сервисная функция для получения ссылки на обложку найденной книги"""

    logger.info("Работа функции для получения ссылки на обложку найденной книги ")

    cover_id = func.get("cover_i")
    if cover_id:
        cover_url = api.get_cover_url(cover_id)
        return cover_url
    else:
        return None
