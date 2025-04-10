import pytest
from unittest.mock import patch, MagicMock
import requests
from src.hh import Parser, HH
from src.file_worker import JsonSaver
from src.vacancy import Vacancy

@pytest.fixture
def mock_file_worker():
    """Фикстура для создания мок-объекта JsonSaver"""
    return MagicMock(spec=JsonSaver)

def test_parser_abstract():
    """Проверка, что Parser - абстрактный класс"""
    with pytest.raises(TypeError):
        Parser(MagicMock())

def test_hh_init(mock_file_worker):
    """Проверка инициализации класса HH"""
    hh = HH(mock_file_worker)
    
    assert hh.url == 'https://api.hh.ru/vacancies'
    assert hh.headers == {'User-Agent': 'HH-User-Agent'}
    assert hh.params == {'text': '', 'page': 0, 'per_page': 100}
    assert hh.vacancies == []
    assert hh.file_worker == mock_file_worker

@patch('requests.get')
def test_hh_load_vacancies(mock_get, mock_file_worker):
    """Проверка загрузки вакансий через API HeadHunter"""
    # Настраиваем мок для имитации успешного ответа API
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "items": [
            {
                "id": "123456",
                "name": "Python Developer",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "snippet": {"requirement": "Python, Django, Flask"},
                "alternate_url": "https://hh.ru/vacancy/123456"
            }
        ]
    }
    mock_get.return_value = mock_response
    
    # Патчим метод range, чтобы цикл в load_vacancies выполнился только один раз
    with patch('builtins.range') as mock_range:
        # Настраиваем mock_range, чтобы он возвращал [0] при вызове range(20)
        mock_range.return_value = [0]
        
        hh = HH(mock_file_worker)
        hh.load_vacancies("Python")
    
    # Проверяем, что параметры запроса были установлены правильно
    assert hh.params['text'] == "Python"
    
    # Проверяем, что запрос был отправлен с правильными параметрами
    mock_get.assert_called_with(
        'https://api.hh.ru/vacancies',
        headers={'User-Agent': 'HH-User-Agent'},
        params={'text': 'Python', 'page': 1, 'per_page': 100}
    )
    
    # Проверяем, что вакансии были добавлены в список
    assert len(hh.vacancies) == 1
    assert isinstance(hh.vacancies[0], Vacancy)
    assert hh.vacancies[0].name == "Python Developer"
    assert hh.vacancies[0].url == "https://hh.ru/vacancy/123456"

@patch('requests.get')
def test_hh_load_vacancies_exception(mock_get, mock_file_worker):
    """Проверка обработки исключений при загрузке вакансий"""
    # Настраиваем мок для имитации ошибки
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")
    
    hh = HH(mock_file_worker)
    
    # Проверяем, что исключение обрабатывается
    with pytest.raises(requests.exceptions.RequestException):
        hh.load_vacancies("Python")
    
    # Проверяем, что список вакансий остался пустым
    assert hh.vacancies == []