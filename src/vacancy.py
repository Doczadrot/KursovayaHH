class Vacancy:
    __slots__ = ['name', 'requirements', 'url', 'salary', 'employer']

    def __init__(self, name: str, requirements: str, url: str, salary: dict = None, employer: str = None):
        """Инициализация объекта вакансии.

        Args:
            name (str): Название вакансии
            requirements (str): Требования к кандидату
            url (str): Ссылка на вакансию
            salary (dict, optional): Информация о зарплате
            employer (str, optional): Название работодателя

        Raises:
            ValueError: При некорректном формате зарплаты
        """
        self._validate_salary(salary)
        self.name = name
        self.requirements = requirements
        self.url = url
        self.salary = salary
        self.employer = employer or "Не указан"

    def _validate_salary(self, salary):
        """Проверяет корректность формата зарплаты.

        Args:
            salary (dict or int): Данные о зарплате (словарь или число)

        Raises:
            ValueError: При некорректном формате зарплаты
        """
        if salary:
            if isinstance(salary, (int, float)):
               
                salary = {'from': salary, 'to': None, 'currency': None}
            elif isinstance(salary, dict):
                if not (isinstance(salary.get('from'), (int, float, type(None))) and 
                        isinstance(salary.get('to'), (int, float, type(None))) and 
                        isinstance(salary.get('currency'), (str, type(None)))):
                    raise ValueError("Некорректный формат зарплаты")
            else:
                raise ValueError("Некорректный формат зарплаты")

    def get_min_salary(self) -> int:
        """Возвращает минимальное значение зарплаты.

        Returns:
            int: Минимальное значение зарплаты или 0, если зарплата не указана
        """
        if not self.salary:
            return 0
        return max(self.salary.get('from', 0) or 0, self.salary.get('to', 0) or 0)

    def __lt__(self, other: 'Vacancy') -> bool:
        """Сравнение вакансий по зарплате (меньше)."""
        return self.get_min_salary() < other.get_min_salary()

    def __gt__(self, other: 'Vacancy') -> bool:
        """Сравнение вакансий по зарплате (больше)."""
        return self.get_min_salary() > other.get_min_salary()

    def __eq__(self, other) -> bool:
        """Сравнение вакансий по ссылке (равно).
        
        Две вакансии считаются одинаковыми, если у них одинаковые ссылки.
        """
        if not isinstance(other, Vacancy):
            return False
        return self.url == other.url
    
    def __hash__(self) -> int:
        """Хеш-функция для вакансии, основанная на ссылке.
        
        Returns:
            int: Хеш-значение ссылки на вакансию
        """
        return hash(self.url)

    def to_dict(self) -> dict:
        """Сериализует объект вакансии в словарь.

        Returns:
            dict: Словарь с данными вакансии
        """
        return {
            'name': self.name,
            'requirements': self.requirements,
            'url': self.url,
            'salary': self.salary,
            'employer': self.employer
        }

    @classmethod
    def cast_to_object_list(cls, data: list) -> list['Vacancy']:
        """Преобразует список словарей в список объектов Vacancy.
        
        Args:
            data (list): Список словарей с данными вакансий
            
        Returns:
            list[Vacancy]: Список объектов Vacancy
        """
        result = []
        for item in data:
            # Преобразуем данные API в формат, подходящий для создания объекта Vacancy
            vacancy_data = {
                'name': item.get('name', ''),
                'requirements': item.get('snippet', {}).get('requirement', '') if item.get('snippet') else '',
                'url': item.get('alternate_url', ''),
                'salary': item.get('salary', None),
                'employer': item.get('employer') if isinstance(item.get('employer'), str) else 
                           item.get('employer', {}).get('name', 'Не указан') if item.get('employer') else 'Не указан'
            }
            result.append(cls(**vacancy_data))
        return result