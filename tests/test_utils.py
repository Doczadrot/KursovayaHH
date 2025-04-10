import pytest
from src.utils import sort_vacancies, get_vacancies_by_salary
from src.vacancy import Vacancy

@pytest.fixture
def test_vacancies():
    """Фикстура для создания списка тестовых вакансий"""
    return [
        Vacancy(
            name="Python Developer", 
            requirements="Python, Django", 
            url="https://test.com/vacancy/1", 
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            employer="Company A"
        ),
        Vacancy(
            name="Java Developer", 
            requirements="Java, Spring", 
            url="https://test.com/vacancy/2", 
            salary={"from": 120000, "to": 180000, "currency": "RUR"},
            employer="Company B"
        ),
        Vacancy(
            name="Frontend Developer", 
            requirements="JavaScript, React", 
            url="https://test.com/vacancy/3", 
            salary={"from": 90000, "to": 130000, "currency": "RUR"},
            employer="Company C"
        )
    ]

def test_sort_vacancies(test_vacancies):
    """Проверка сортировки вакансий по зарплате"""
    sorted_vacancies = sort_vacancies(test_vacancies)
    
    # Проверка, что вакансии отсортированы по убыванию зарплаты
    assert sorted_vacancies[0].name == "Java Developer"  # 120000-180000
    assert sorted_vacancies[1].name == "Python Developer"  # 100000-150000
    assert sorted_vacancies[2].name == "Frontend Developer"  # 90000-130000

def test_get_vacancies_by_salary_valid_range(test_vacancies):
    """Проверка фильтрации вакансий по диапазону зарплат (валидный диапазон)"""
    # Диапазон, который включает только Python Developer и Frontend Developer
    filtered_vacancies = get_vacancies_by_salary(test_vacancies, "90000-150000")
    
    # Проверяем, что отфильтрованы только вакансии с зарплатой в диапазоне 90000-150000
    assert len(filtered_vacancies) == 2
    # Проверяем, что в результате есть нужные вакансии
    assert any(v.name == "Python Developer" for v in filtered_vacancies)
    assert any(v.name == "Frontend Developer" for v in filtered_vacancies)

def test_get_vacancies_by_salary_empty_range(test_vacancies):
    """Проверка фильтрации вакансий по пустому диапазону зарплат"""
    filtered_vacancies = get_vacancies_by_salary(test_vacancies, "")
    
    # Должны вернуться все вакансии
    assert len(filtered_vacancies) == 3

def test_get_vacancies_by_salary_invalid_format(test_vacancies):
    """Проверка фильтрации вакансий по некорректному формату диапазона"""
    # Некорректный формат диапазона
    filtered_vacancies = get_vacancies_by_salary(test_vacancies, "invalid_format")
    
    # Должны вернуться все вакансии
    assert len(filtered_vacancies) == 3

def test_get_vacancies_by_salary_no_matches(test_vacancies):
    """Проверка фильтрации вакансий по диапазону без совпадений"""
    # Диапазон, который не включает ни одну вакансию
    filtered_vacancies = get_vacancies_by_salary(test_vacancies, "200000-250000")
    
    # Не должно быть совпадений
    assert len(filtered_vacancies) == 0