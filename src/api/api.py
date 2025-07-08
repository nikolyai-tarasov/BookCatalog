from abc import ABC, abstractmethod


class BaseApiClient(ABC):
    """ Абстрактный класс для выделения интерфейсов API"""

    @abstractmethod
    def get_response(self,*args, **kwargs):
        pass

    @abstractmethod
    def send_request(self, *args, **kwargs):
        pass



class BaseApiOpenLibrary(BaseApiClient, ABC):
    """ Абстрактный класс расширающий функцианал для API"""

    @abstractmethod
    def search(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_book_details(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_cover_url(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_rating(self, *args, **kwargs):
        pass







