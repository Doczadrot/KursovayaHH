import requests


from abc import ABC, abstractmethod


class ApiConnector(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Абстрактный метод для подключения к API."""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> list[dict]:
        """Абстрактный метод для получения вакансий.

        Args:
            keyword (str): Ключевое слово для поиска

        Returns:
            list[dict]: Список вакансий в формате словарей
        """
        pass


class HeadHunterApi(ApiConnector):
    def __init__(self):
        self._base_url = "https://api.hh.ru/"
        
    def connect(self) -> None:
        """Реализация абстрактного метода для подключения к API."""
        client_id = "id token"
        print("Подколючаемся к API")

    def get_vacancies(self, keyword: str) -> list[dict]:
        url = "https://api.hh.ru/vacancies"  # URL-адрес для запроса вакансий на hh.ru
        params = {"text": keyword}  # Параметры запроса. Здесь мы указываем ключевое слово для поиска.

        try:  # Блок try позволяет нам обработать возможные ошибки при выполнении запроса.
            response = requests.get(url,params=params)  # Отправляем GET-запрос на указанный URL с заданными параметрами.
            response.raise_for_status()  # Эта строка проверяет, что запрос был выполнен успешно
            # (код ответа 200). Если нет, возникнет ошибка.
            vacancies_data = response.json()  # Преобразуем полученный от сервера ответ в формате JSON в словарь Python.
            vacancies_list = vacancies_data.get("items",[])  # Извлекаем список вакансий
            # из полученного словаря по ключу "items". Если ключ отсутствует, возвращаем пустой список.
            return vacancies_list  # Возвращаем полученный список вакансий.
        except requests.exceptions.RequestException as e:  # Если во время
            # выполнения запроса произошла ошибка...
            print(f"Ошибка при получении вакансий: {e}")  # ...выводим сообщение об ошибке.
            return []  # ...и возвращаем пустой список вакансий.