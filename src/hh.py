import requests
from abc import ABC, abstractmethod
from src.vacancy import Vacancy


class Parser(ABC):
    """Базовый класс для парсеров вакансий"""
    
    def __init__(self, file_worker):
        self.file_worker = file_worker
        
    @abstractmethod
    def load_vacancies(self, keyword):
        """Загружает вакансии по ключевому слову"""
        pass


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """

    def __init__(self, file_worker):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        super().__init__(file_worker)

    def load_vacancies(self, keyword):
        self.params['text'] = keyword
        for _ in range(20):
            response = requests.get(self.url, headers=self.headers, params=self.params)
            response.raise_for_status()
            data = response.json()
            for item in data['items']:
                salary = item.get('salary')
                self.vacancies.append(Vacancy(
                    name=item['name'],
                    url=item['alternate_url'],
                    salary=salary['from'] if salary else 0,
                    requirements=item['snippet']['requirement'],
                ))
            self.params['page'] += 1