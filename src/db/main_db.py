import os
from src.library_catalog.service import (open_library_book, open_library_cover,
                                         open_library_rating, open_library_description)
from src.db.db import BookRepository
from src.library_catalog.models import NewBook, BookUpdate
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from src.logger.logger import setup_logger

load_dotenv(override=True)
logger = setup_logger("endpoint.db")
db = BookRepository(f'postgresql://{os.getenv('USER')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}/{os.getenv('DB_NAME')}')
app = FastAPI()

@app.get("/get_books_db")
def get_books(skip: int = 0, limit: int = 10):
    """ Эндпоинт запроса всех книг из БД """

    logger.info("Работа эндпоинта запроса всех книг из БД")
    try:
        books = db.get_book(skip=skip, limit=limit)
        return books
    except Exception as e:
        return f"Ошибка при получении всех книг из БД - {e}"


@app.post("/create_books_db")
def create_books(book:NewBook):
    """ Эндпоинт создания книги """

    logger.info("Работа эндпоинта создания книг в БД")
    try:
        # Реализация обновления данных через сервис OpenLibrary
        func = open_library_book(book.title)
        description = open_library_description(func)
        rating = open_library_rating(func)
        cover_url = open_library_cover(func)

        new_book = db.add_book(book.title, book.author, book.year_publication, book.genre, book.number_pages, description,
                               rating, cover_url, book.access )
        return new_book
    except Exception as e:
        return f"Ошибка при создании книги - {e}"

@app.get("/get_book_db/{book_id}")
def get_book_db(book_id: int):
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
def update_book_db(book_id: int, book_update: BookUpdate):
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
def delete_book_db(book_id: int):
    """ Эндпоинт удаления книги из БД """

    logger.info("Работа эндпоинта удаления книги в БД")
    try:
        book_db = db.delete_book(book_id)
        if book_db:
            return "Книга удалена"
        raise HTTPException(status_code=404, detail="Книга не найдена")
    except Exception as e:
        return f"Ошибка при удалении книги - {e}"