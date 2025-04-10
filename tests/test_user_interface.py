import pytest
from unittest.mock import patch, MagicMock
from src.user_interface import show_vacancies_from_file, get_vacancies_by_salary, sort_vacancies, print_vacancies
from src.vacancy import Vacancy
from src.file_worker import JsonSaver

@patch('builtins.print')
@patch.object(JsonSaver, 'load_from_file')
def test_show_vacancies_from_file_empty(mock_load, mock_print):
    """Проверка отображения вакансий из файла (пустой файл)"""
    # Настраиваем мок для возврата пустого списка
    mock_load.return_value = []
    
    show_vacancies_from_file("empty_file.json")
    
    # Проверяем, что функция вызвала print с сообщением о пустом файле
    mock_print.assert_called_once()
    args, _ = mock_print.call_args
    assert "Файл не содержит валидных вакансий" in str(args)

def test_get_vacancies_by_salary_valid_range(test_vacancies):
    """Проверка фильтрации вакансий по диапазону зарплат (валидный диапазон)"""
    # Диапазон, который включает только Python Developer
    filtered_vacancies = get_vacancies_by_salary(test_vacancies, "90000-110000")
    
    assert len(filtered_vacancies) == 1
    assert filtered_vacancies[0].name == "Python Developer"

def test_get_vacancies_by_salary_empty_range(test_vacancies):
    """Проверка фильтрации вакансий по пустому диапазону зарплат"""
    filtered_vacancies = get_vacancies_by_salary(test_vacancies, "")
    
    # Должны вернуться все вакансии
    assert len(filtered_vacancies) == 2

def test_get_vacancies_by_salary_invalid_format(test_vacancies):
    """Проверка фильтрации вакансий по некорректному формату диапазона"""
    # Некорректный формат диапазона
    filtered_vacancies = get_vacancies_by_salary(test_vacancies, "invalid_format")
    
    # Должны вернуться все вакансии
    assert len(filtered_vacancies) == 2

def test_sort_vacancies(test_vacancies):
    """Проверка сортировки вакансий по зарплате"""
    sorted_vacancies = sort_vacancies(test_vacancies)
    
    # Проверка, что вакансии отсортированы по убыванию зарплаты
    assert sorted_vacancies[0].name == "Java Developer"  # 120000-180000
    assert sorted_vacancies[1].name == "Python Developer"  # 100000-150000

@patch('builtins.print')
def test_print_vacancies(mock_print, test_vacancies):
    """Проверка вывода информации о вакансиях"""
    print_vacancies(test_vacancies)
    
    # Проверяем, что функция вызвала print для каждой вакансии
    assert mock_print.call_count >= len(test_vacancies)
    # Проверяем, что в выводе есть названия вакансий
    printed_text = ''.join(str(args) for args, _ in mock_print.call_args_list)
    assert "Python Developer" in printed_text
    assert "Java Developer" in printed_text