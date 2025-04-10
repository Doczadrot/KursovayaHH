from abc import ABC, abstractmethod
import json
from src.vacancy import Vacancy

class Saver(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass

    @abstractmethod
    def filter_vacancies(self, criteria):
        pass

class JsonSaver(Saver):
    def load_from_file(self) -> list[Vacancy]:
        """
        Загружает и валидирует вакансии из JSON-файла
        
        Returns:
            list[Vacancy]: Список валидных объектов Vacancy
        
        Raises:
            FileNotFoundError: Если файл не существует
        """
        try:
            with open(self.__file__, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        validated_vacancies = []
        for item in data:
            try:
                # Валидация обязательных полей
                if not all(key in item for key in ('name', 'url')):
                    raise ValueError("Отсутствуют обязательные поля")
                
                # Нормализация данных о зарплате
                salary = item.get('salary')
                if salary and isinstance(salary, dict):
                    salary = {
                        'from': salary.get('from', 0),
                        'to': salary.get('to', 0),
                        'currency': salary.get('currency', 'RUB')
                    }

                validated_vacancies.append(Vacancy(
                    name=item['name'],
                    requirements=item.get('requirements', ''),
                    url=item['url'],
                    salary=salary,
                    employer=item.get('employer', '')
                ))
            except (KeyError, ValueError, TypeError) as e:
                print(f"Ошибка валидации: {str(e)}")
        
        return validated_vacancies
        
    def __init__(self, filename: str):
        """
        Инициализирует объект для работы с JSON-файлом
        
        Args:
            filename (str): Путь к файлу для сохранения вакансий
        """
        self.__file__ = filename
        # Создаем файл если не существует
        open(filename, 'a+', encoding='utf-8').close()
        self.vacancies = self.load_from_file()

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в хранилище
        
        Args:
            vacancy (Vacancy): Объект вакансии для добавления
        """
        if vacancy in self.vacancies:
            # Пропускаем существующие вакансии вместо вызова исключения
            return
        self.vacancies.append(vacancy)
        self._save_to_file()

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из хранилища
        
        Args:
            vacancy (Vacancy): Объект вакансии для удаления
        """
        self.vacancies = [v for v in self.vacancies if v.url != vacancy.url]
        self._save_to_file()

    def filter_vacancies(self, criteria) -> list[Vacancy]:
        """
        Фильтрует вакансии по заданному критерию
        
        Args:
            criteria: Функция-критерий для фильтрации вакансий
            
        Returns:
            list[Vacancy]: Отфильтрованный список вакансий
        """
        return [v for v in self.vacancies if criteria(v)]
        
    def _save_to_file(self) -> None:
        """
        Сохраняет вакансии в JSON-файл
        """
        vacancies_data = [vacancy.to_dict() for vacancy in self.vacancies]
        with open(self.__file__, "w", encoding="utf-8") as file:
            json.dump(vacancies_data, file, ensure_ascii=False, indent=4)