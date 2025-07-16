from src.library_catalog.app.api.api import  BaseApiOpenLibrary
import os
import requests
from src.library_catalog.app.logger.logger import setup_logger

logger = setup_logger("class.OpenLibraryAPI")


class OpenLibraryAPI(BaseApiOpenLibrary):
    """ Класс для раюоты с сервисос OpenLibrary для обновления данных о книгах """

    BASE_URL = os.getenv("OPENLIBRARY_BASE_URL", "https://openlibrary.org")
    COVERS_URL = os.getenv("OPENLIBRARY_COVERS_URL", "https://covers.openlibrary.org/b")

    def __init__(self):
        self.session = requests.Session()

    def get_response(self, endpoint: str, params: dict = None):
        """ Метод для запроса данных у OpenLibrary  """

        logger.info("Работа метода запроса данных, класса OpenLibraryAPI")
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Ошибка при запросе - {e}"

    def search(self, query: str):
        """ Метод для поиска книг в сервисе  """

        logger.info("Работа метода поиска книги, класса OpenLibraryAPI")
        try:
            result = self.get_response("/search.json", {"q": query})
            if result and result.get("numFound", 0) > 0:
                return result["docs"][0]
            return None
        except Exception as e:
            return f"Ошибка при запросе{e}"

    def get_book_details(self, key: str):
        """ Метод для получения деталей о книги """

        logger.info("Работа метода запроса деталей книги, класса OpenLibraryAPI")
        try:
            book_detail = self.get_response(f"{key}.json")
            return book_detail

        except Exception as e:
            return f"Ошибка при запросе деталей о книге - {e}"


    def get_cover_url(self, cover_id: int, size="M"):
        """ Метод получения ссылки на обложку книги """

        logger.info("Работа метода запроса ссылки на обложку книги, класса OpenLibraryAPI")
        return f"{self.COVERS_URL}/b/id/{cover_id}-{size}.jpg"

    def get_rating(self, work_key: str):
        """ Метод получения рейтинга книги """

        logger.info("Работа метода запроса рейтинга книг, класса OpenLibraryAPI")
        try:
            result = self.get_response(f"/{work_key}/ratings.json")
            if result and "summary" in result:
                return result["summary"].get("average")
            return None

        except Exception as e:
            return f"Ошибка при запросе рейтинга о книге - {e}"

    def close(self):
        """ Метод закрытия ссесии """
        logger.info("Работа метода закрытия ссесии, класса OpenLibraryAPI")
        self.session.close()

    def send_request(self, *args, **kwargs):
        """ Абстрактный метод обновления данных """
        pass
