from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from src.library_catalog.app.db.models_db import Base
from dotenv import load_dotenv
import os


load_dotenv(override=True)



class DataBaseSession:
    """ Класс для создания движка и сессии БД """

    def __init__(self):
        """ Класс конструктор """

        self.db = f'postgresql://{os.getenv('USER')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}/{os.getenv('DB_NAME')}'
        self.engine = create_engine(self.db)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """ Класс создания сессии """

        return self.SessionLocal()



