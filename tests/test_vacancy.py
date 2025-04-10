import pytest
from src.vacancy import Vacancy

# Тесты для класса Vacancy

def test_vacancy_creation():
    """Проверка создания объекта вакансии"""
    vac = Vacancy(
        name="Python Developer",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        url="https://hh.ru/vacancy/123",
        requirements="Опыт работы от 3 лет",
        employer="XYZ Company"
    )
    assert vac.name == "Python Developer"
    assert vac.salary["from"] == 100000
    assert vac.salary["to"] == 150000
    assert vac.salary["currency"] == "RUR"
    assert vac.url == "https://hh.ru/vacancy/123"
    assert vac.requirements == "Опыт работы от 3 лет"
    assert vac.employer == "XYZ Company"


def test_vacancy_default_employer():
    """Проверка значения по умолчанию для работодателя"""
    vac = Vacancy(
        name="Python Developer",
        requirements="Опыт работы от 3 лет",
        url="https://hh.ru/vacancy/123",
        salary={"from": 100000}
    )
    assert vac.employer == "Не указан"


def test_validate_salary_valid():
    """Проверка валидации корректной зарплаты"""
    # Различные варианты корректных данных о зарплате
    valid_salaries = [
        {"from": 100000, "to": 150000, "currency": "RUR"},
        {"from": None, "to": 150000, "currency": "RUR"},
        {"from": 100000, "to": None, "currency": "RUR"},
        {"from": 100000, "to": 150000, "currency": None},
        None  # Зарплата может быть None
    ]
    
    for salary in valid_salaries:
        # Не должно вызывать исключений
        Vacancy(name="Test", requirements="Test", url="test", salary=salary)


def test_validate_salary_invalid():
    """Проверка валидации некорректной зарплаты"""
    invalid_salaries = [
        {"from": "100000", "to": 150000, "currency": "RUR"},  # from не число
        {"from": 100000, "to": "150000", "currency": "RUR"},  # to не число
        {"from": 100000, "to": 150000, "currency": 123}  # currency не строка
    ]
    
    for salary in invalid_salaries:
        with pytest.raises(ValueError, match="Некорректный формат зарплаты"):
            Vacancy(name="Test", requirements="Test", url="test", salary=salary)


def test_get_min_salary():
    """Проверка метода получения минимальной зарплаты"""
    test_cases = [
        ({"from": 100000, "to": 150000}, 150000),  # Берется максимальное значение
        ({"from": None, "to": 150000}, 150000),
        ({"from": 100000, "to": None}, 100000),
        ({"from": None, "to": None}, 0),
        (None, 0)  # Если зарплата не указана
    ]
    
    for salary, expected in test_cases:
        vac = Vacancy(name="Test", requirements="Test", url="test", salary=salary)
        assert vac.get_min_salary() == expected


def test_vacancy_comparison_lt():
    """Проверка сравнения вакансий (меньше)"""
    vac1 = Vacancy(name="Test1", requirements="Test", url="test1", salary={"from": 100000})
    vac2 = Vacancy(name="Test2", requirements="Test", url="test2", salary={"from": 120000})
    assert vac1 < vac2


def test_vacancy_comparison_gt():
    """Проверка сравнения вакансий (больше)"""
    vac1 = Vacancy(name="Test1", requirements="Test", url="test1", salary={"from": 100000})
    vac2 = Vacancy(name="Test2", requirements="Test", url="test2", salary={"from": 120000})
    assert vac2 > vac1


def test_vacancy_equality():
    """Проверка сравнения вакансий на равенство"""
    vac1 = Vacancy(name="Test1", requirements="Test", url="same_url", salary={"from": 100000})
    vac2 = Vacancy(name="Test2", requirements="Different", url="same_url", salary={"from": 120000})
    vac3 = Vacancy(name="Test3", requirements="Test", url="different_url", salary={"from": 100000})
    
    # Вакансии с одинаковыми URL считаются одинаковыми
    assert vac1 == vac2
    assert vac1 != vac3
    assert vac1 != "not_a_vacancy"  # Сравнение с другим типом


def test_vacancy_hash():
    """Проверка хеш-функции для вакансий"""
    vac1 = Vacancy(name="Test1", requirements="Test", url="same_url", salary={"from": 100000})
    vac2 = Vacancy(name="Test2", requirements="Different", url="same_url", salary={"from": 120000})
    
    # Хеши вакансий с одинаковыми URL должны быть одинаковыми
    assert hash(vac1) == hash(vac2)
    assert hash(vac1) == hash("same_url")


def test_to_dict():
    """Проверка сериализации вакансии в словарь"""
    vac = Vacancy(
        name="Python Developer",
        requirements="Опыт работы от 3 лет",
        url="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        employer="XYZ Company"
    )
    
    vac_dict = vac.to_dict()
    assert vac_dict["name"] == "Python Developer"
    assert vac_dict["requirements"] == "Опыт работы от 3 лет"
    assert vac_dict["url"] == "https://hh.ru/vacancy/123"
    assert vac_dict["salary"] == {"from": 100000, "to": 150000, "currency": "RUR"}
    assert vac_dict["employer"] == "XYZ Company"


def test_cast_to_object_list():
    """Проверка преобразования списка словарей в список объектов Vacancy"""
    data = [
        {
            "name": "Python Developer",
            "requirements": "Опыт работы от 3 лет",
            "url": "https://hh.ru/vacancy/123",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "employer": "XYZ Company"
        },
        {
            "name": "Java Developer",
            "requirements": "Опыт работы от 5 лет",
            "url": "https://hh.ru/vacancy/456",
            "salary": {"from": 150000, "to": 200000, "currency": "RUR"},
            "employer": "ABC Company"
        }
    ]
    
    vacancies = Vacancy.cast_to_object_list(data)
    
    assert len(vacancies) == 2
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].name == "Python Developer"
    assert vacancies[1].name == "Java Developer"