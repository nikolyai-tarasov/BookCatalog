from abc import ABC, abstractmethod


class DataBase(ABC):
    """ Абстрактный класс для работы базы данных """

    @abstractmethod
    def add_book(self, *args, **kwargs):
        """ Абстрактный метод добавления книги """
        pass

    @abstractmethod
    def get_book(self,*args, **kwargs):
        """ Абстрактный метод запроса книг """
        pass

    @abstractmethod
    def get_book_index(self, *args, **kwargs):
        """ Абстрактный метод запроса книг по индексу """
        pass


    @abstractmethod
    def put_book(self,*args, **kwargs):
        """ Абстрактный метод люновления книг """
        pass

    @abstractmethod
    def delete_book(self, *args, **kwargs):
        """ Абстрактный метод удаления книг """
        pass