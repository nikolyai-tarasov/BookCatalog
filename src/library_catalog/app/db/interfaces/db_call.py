from src.library_catalog.app.db.db import BookRepository


def get_repo() -> BookRepository:
    """ Функция вызова класса раюоты с БД"""
    return BookRepository()