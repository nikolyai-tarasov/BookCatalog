from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float

Base = declarative_base()

class Books(Base):
    """ Схема для создания таблицы в БД """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    year_publication = Column(Integer)
    genre = Column(String)
    number_pages = Column(Integer)
    access = Column(Boolean, default=True)
    description = Column(String)
    rating = Column(Float)
    cover_url = Column(String)
