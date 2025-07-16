from typing import Optional

from src.library_catalog.app.db.interfaces.db_call import get_repo
from src.library_catalog.app.service.service_open_library import (open_library_book, open_library_cover,
                                                                   open_library_rating, open_library_description)
from src.library_catalog.app.db.db import BookRepository
from src.library_catalog.app.catalog.models import NewBook, BookUpdate
from fastapi import FastAPI, HTTPException, Depends

from src.library_catalog.app.logger.logger import setup_logger

logger = setup_logger("endpoint.db")

app = FastAPI()


@app.get("/get_books_db")
def get_books(skip: int = 0, limit: int = 10, db:  BookRepository = Depends(get_repo)):
    """ Эндпоинт запроса всех книг из БД """

    logger.info("Работа эндпоинта запроса всех книг из БД")
    try:
        books = db.get_book(skip=skip, limit=limit)
        return books
    except Exception as e:
        return f"Ошибка при получении всех книг из БД - {e}"


@app.post("/create_books_db")
def create_books(book: NewBook,  db:  BookRepository = Depends(get_repo)) -> Optional[dict, str]:
    """ Эндпоинт создания книги """

    logger.info("Работа эндпоинта создания книг в БД")
    try:
        # Реализация обновления данных через сервис OpenLibrary
        func = open_library_book(book.title)
        description = open_library_description(func)
        rating = open_library_rating(func)
        cover_url = open_library_cover(func)

        new_book = db.add_book(book.title, book.author, book.year_publication, book.genre, book.number_pages,
                               description,
                               rating, cover_url, book.access)
        return new_book
    except Exception as e:
        return f"Ошибка при создании книги - {e}"


@app.get("/get_book_db/{book_id}")
def get_book_db(book_id: int,  db:  BookRepository = Depends(get_repo)) -> Optional[dict, str]:
    """ Эндпоинт поиска книги по индексу в БД """

    logger.info("Работа эндпоинта поиска книг в БД по индексу")
    try:
        book = db.get_book_index(book_id - 1)
        if not book:
            raise HTTPException(status_code=404, detail="Книга не найдена")
        return book
    except Exception as e:
        return f"Ошибка при поиске книги по индексу - {e}"


@app.put("/update_book_db/{book_id}")
def update_book_db(book_id: int, book_update: BookUpdate,  db:  BookRepository = Depends(get_repo)) -> Optional[None, str]:
    """ Эндпоинт обновления книги  """

    logger.info("Работа эндпоинта обновления книги в БД")
    try:
        book_db = db.put_book(book_id, book_update)
        if book_db:
            return "Книга обновлена"
        raise HTTPException(status_code=404, detail="Книга не найдена")
    except Exception as e:
        return f"Ошибка при обновлении книги - {e}"


@app.delete("/delete_book_db/{book_id}")
def delete_book_db(book_id: int,  db:  BookRepository = Depends(get_repo)) -> Optional[None, str]:
    """ Эндпоинт удаления книги из БД """

    logger.info("Работа эндпоинта удаления книги в БД")
    try:
        book_db = db.delete_book(book_id)
        if book_db:
            return "Книга удалена"
        raise HTTPException(status_code=404, detail="Книга не найдена")
    except Exception as e:
        return f"Ошибка при удалении книги - {e}"
