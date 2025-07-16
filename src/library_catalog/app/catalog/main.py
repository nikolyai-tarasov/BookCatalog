import random

from typing import Optional

from fastapi.params import Depends

from src.library_catalog.app.catalog.models import NewBook, BookUpdate, BaseBook
from fastapi import FastAPI, HTTPException
from src.library_catalog.app.service.service_file import open_file_r, open_file_w
from src.library_catalog.app.service.service_open_library import (open_library_book, open_library_cover,
                                                                   open_library_rating, open_library_description)
from pathlib import Path
from src.library_catalog.app.api.json_bin_repository import JsonBin
from src.library_catalog.app.logger.logger import setup_logger

logger = setup_logger("endpoint")

FILE_PATH = Path("src/data/books.json")

app = FastAPI()


@app.get("/get_books_json_io")
def get_books(json_io: JsonBin = Depends(JsonBin)) -> dict[str]:
    """ Эндпоинт запроса всех книг из хранилища JsonBin.io"""

    logger.info("Работа эндпоинта запроса всех книг из хранилища JsonBin.io ")
    return json_io.get_response()

@app.get("/get_books")
def get_books(genre: Optional[str] = None) -> list[dict[str]]:
    """ Эндпоинт получение всех книг из файла JSON с возможность фильтрации по жанру """

    logger.info("Работа эндпоинта запроса всех книг из файла 'books.json'")
    books = open_file_r(FILE_PATH)
    if genre:
        return [book for book in books if book['genre'] == genre]
    return books


@app.get("/book/{book_id}")
def get_book(book_id: int) -> dict[str]:
    """ Эндпоинт поиска книги по индексу в файле JSON """

    logger.info("Работа эндпоинта запроса книги из файла 'books.json' по индексу")
    data = open_file_r(FILE_PATH)
    for i in data:
        if book_id == i["id"]:
            return i

    raise HTTPException(status_code=404, detail="Книга не найдена")


@app.post("/add_book")
def add_book(new_book: NewBook, json_bd: JsonBin = Depends(JsonBin)) -> BaseBook:
    """ Эндпоинт создания книги """

    logger.info("Работа эндпоинта добавление книги в файла 'books.json'")
    func = open_library_book(new_book.title)
    books = open_file_r(FILE_PATH)
    next_id = random.randint(1, 10000)

    book_create = {"id": next_id,
                   "title": new_book.title,
                   "author": new_book.author,
                   "year_publication": new_book.year_publication,
                   "genre": new_book.genre,
                   "number_pages": new_book.number_pages,
                   "access": new_book.access,
                   "description": open_library_description(func),
                   "rating": open_library_rating(func),
                   "cover_url": open_library_cover(func)
                   }


    books.append(book_create)
    open_file_w(FILE_PATH, books)
    json_bd.send_request(books)
    return BaseBook(**book_create)


@app.put("/update_book/{book_id}")
def update_book(book_id: int, book_update: BookUpdate) -> str:
    """ Эндпоинт обновления книги """

    logger.info("Работа эндпоинта обновления книги из файла 'books.json'")
    data = open_file_r(FILE_PATH)
    for book in data:
        if book["id"] == book_id:
            update_data = book_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                book[key] = value
            break

    open_file_w(FILE_PATH, data)
    return "Book updated"


@app.delete("/delete_book/{book_id}")
def delete_book(book_id: int) -> Optional[None, str]:
    """ Эндпоинт удаления книги """

    logger.info("Работа эндпоинта удаления книги из файла 'books.json'")
    data = open_file_r(FILE_PATH)
    for i, book in enumerate(data):
        if book["id"] == book_id:
            rem_book = data.pop(i)
            open_file_w(FILE_PATH, data)
            return f"Book {rem_book['title']} delete"
        else:
            raise HTTPException(status_code=404, detail="Книга не найдена")
