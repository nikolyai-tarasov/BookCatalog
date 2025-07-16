import os
import requests
from dotenv import load_dotenv
from src.library_catalog.app.api.api import BaseApiClient
from src.library_catalog.app.logger.logger import setup_logger

load_dotenv(override=True)
logger = setup_logger("class.JsonBin")


class JsonBin(BaseApiClient):
    """ Класс для работы с хранилищем JsonBin.io """

    def __init__(self):
        self.url = os.getenv('URL')
        self.master_key = os.getenv('API_KEY')
        self.bin_id = os.getenv('BIN_ID')
        self.access_key = os.getenv("ACCESS-KEY")
        self.full_url = f'{self.url}/{self.bin_id}'
        self.headers_put = {
            "Content-Type": "application/json",
            "X-Master-Key": self.master_key,
        }
        self.headers_get = {
            "X-Master-Key": self.master_key,
        }

    def get_response(self):
        """ Метод для запроса данных у хранилища """
        logger.info("Работа метода запроса данных из хранилища, класса JsonBin")
        try:
            response = requests.get(url=f"{self.full_url}/latest", headers=self.headers_get, json=None)
            if response.status_code == 200:
                data = response.json()
                return data

        except Exception as e:
            return f"Ошибка при запросе к хранилищу - {e}"




    def send_request(self, up_data):
        """ Метод обновления данных хранилища """
        logger.info("Работа метода обновления хранилища, класса JsonBin")
        try:
            data = {'library': up_data}
            response = requests.put(url=self.full_url, headers=self.headers_put, json=data)
            if response.status_code == 200:
                return "Успешно"
        except Exception as e:
            return f"Ошибка при обновлении данных в хранилище {e}"
