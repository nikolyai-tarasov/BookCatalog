from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from src.db.models_db import Base,Books
from src.logger.logger import setup_logger

logger = setup_logger("db.class.BookRepository")


class BookRepository:
    """ Класс для работы с базой данных Postgresql """

    def __init__(self, db_url: str):
        """ Метод инициализации класса """

        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """ Метод создания ссесии """

        logger.info("Работа метода открытия ссесии с БД")
        return self.SessionLocal()

    def add_book(self, title: str, author: str,
                 year_publication: int, genre: str,
                 number_pages: int, description: str, rating: float, cover_url: str,
                 access: bool = True) -> Books:
        """ Метод добавления новой книги в БД """

        logger.info("Работа метода создания книги в БД")
        session = self.get_session()
        try:
            book = Books(title=title,
                         author=author,
                         year_publication=year_publication,
                         genre=genre,
                         number_pages=number_pages,
                         access=access,
                         description=description,
                         rating=rating,
                         cover_url=cover_url
                         )
            session.add(book)
            session.commit()
            session.refresh(book)
            return book
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_book(self, skip=0, limit=10):
        """ Метод запроса книг из БД """

        logger.info("Работа метода запроса всех книг из БД")
        session = self.get_session()
        try:
            return session.query(Books).offset(skip).limit(limit).all()
        finally:
            session.close()

    def get_book_index(self, index: int):
        """ Метод запроса книги по индексу из БД """

        logger.info("Работа метода поиска книги в БД")

        session = self.get_session()
        try:
            books = session.query(Books).order_by(Books.id).all()
            if index < 0 or index >= len(books):
                return None
            return books[index]
        finally:
            session.close()

    def put_book(self, index, update_data):
        """ Метод обновления книги  """
        logger.info("Работа метода удаления книги из БД")

        session = self.get_session()
        try:
            book = session.query(Books).filter(Books.id == index).first()
            if not book:
                return False

            for key, val in update_data.dict().items():
                setattr(book, key, val)
            session.commit()
            return True

        finally:
            session.close()

    def delete_book(self, book_id):
        """ Метод удаления книги из БД """
        logger.info("Работа метода удаления книги из БД")

        session = self.get_session()
        try:
            book = session.query(Books).filter(Books.id == book_id).first()
            if book:
                session.delete(book)
                session.commit()
                return True
            return False
        finally:
            session.close()
