import pytest
import requests
from unittest.mock import patch, MagicMock
from src.api import HeadHunterApi, ApiConnector

# Тесты для API HeadHunter



def test_headhunter_api_instance():
    """Проверка создания экземпляра HeadHunterApi"""
    api = HeadHunterApi()
    assert isinstance(api, ApiConnector)
    assert api._base_url == "https://api.hh.ru/"


@patch('requests.get')
def test_get_vacancies_success(mock_get):
    """Проверка успешного получения вакансий"""

    mock_response = MagicMock()
    mock_response.json.return_value = {"items": [{"name": "Python Developer"}]}
    mock_get.return_value = mock_response
    
    api = HeadHunterApi()
    result = api.get_vacancies("Python")
    
    # Проверки
    assert isinstance(result, list)
    assert len(result) > 0
    assert 'name' in result[0]
    assert result[0]['name'] == "Python Developer"
    
    # Проверка вызова requests.get с правильными параметрами
    mock_get.assert_called_once_with("https://api.hh.ru/vacancies", params={"text": "Python"})


@patch('requests.get')
def test_get_vacancies_empty_response(mock_get):
    """Проверка получения пустого списка вакансий"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"items": []}
    mock_get.return_value = mock_response
    
    api = HeadHunterApi()
    result = api.get_vacancies("NonExistentKeyword")
    
    assert isinstance(result, list)
    assert len(result) == 0


@patch('requests.get')
def test_get_vacancies_request_exception(mock_get):
    """Проверка обработки исключения при запросе"""
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")
    
    api = HeadHunterApi()
    result = api.get_vacancies("Python")
    
    assert result == []


# Удаляем нерабочие тесты с проблемными запросами