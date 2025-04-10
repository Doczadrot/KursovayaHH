import json
import pytest
from src.file_worker import JsonSaver, Saver
from src.vacancy import Vacancy

@pytest.fixture
def temp_file(tmp_path):
    """Фикстура для создания временного файла"""
    return tmp_path / "test_vacancies.json"

def test_saver_abstract():
    """Проверка, что Saver - абстрактный класс"""
    with pytest.raises(TypeError):
        Saver()


def test_json_saver_init(temp_file):
    """Проверка инициализации JsonSaver"""
    saver = JsonSaver(temp_file)
    assert saver.__file__ == temp_file
    assert isinstance(saver.vacancies, list)
    assert len(saver.vacancies) == 0

def test_add_vacancy(temp_file, test_vacancy):
    """Проверка добавления вакансии"""
    saver = JsonSaver(temp_file)
    saver.add_vacancy(test_vacancy)
    
    # Проверка, что вакансия добавлена в память
    assert len(saver.vacancies) == 1
    assert saver.vacancies[0] == test_vacancy
    
    # Проверка, что вакансия сохранена в файл
    with open(temp_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]['name'] == "Test Vacancy"

def test_add_vacancy_duplicate(temp_file, test_vacancy):
    """Проверка добавления дубликата вакансии"""
    saver = JsonSaver(temp_file)
    saver.add_vacancy(test_vacancy)
    
    # Получаем текущее количество вакансий
    initial_count = len(saver.vacancies)
    
    # Попытка добавить ту же вакансию должна быть проигнорирована
    saver.add_vacancy(test_vacancy)
    
    # Проверяем, что количество вакансий не изменилось
    assert len(saver.vacancies) == initial_count

def test_delete_vacancy(temp_file, test_vacancy):
    """Проверка удаления вакансии"""
    saver = JsonSaver(temp_file)
    saver.add_vacancy(test_vacancy)
    assert len(saver.vacancies) == 1
    
    saver.delete_vacancy(test_vacancy)
    assert len(saver.vacancies) == 0
    
    # Проверка, что вакансия удалена из файла
    with open(temp_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert len(data) == 0

def test_filter_vacancies(temp_file):
    """Проверка фильтрации вакансий"""
    # Очищаем файл перед тестом, чтобы избежать накопления вакансий
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write('[]')
    
    # Создаем новый экземпляр JsonSaver с пустым файлом
    saver = JsonSaver(temp_file)
    
    # Добавляем тестовые вакансии с разными требованиями
    test_vacancies = [
        Vacancy("Python Developer", "Python experience", "python.com", {'from': 100000, 'to': 150000, 'currency': 'RUB'}),
        Vacancy("Java Developer", "Java experience", "java.com", {'from': 90000, 'to': 120000, 'currency': 'RUB'})
    ]
    for vac in test_vacancies:
        saver.add_vacancy(vac)
    
    # Фильтрация по Python в требованиях
    filtered = saver.filter_vacancies(lambda v: "Python" in v.requirements)
    assert len(filtered) == 1
    assert filtered[0].name == "Python Developer"
    
    # Фильтрация по Java в требованиях
    filtered = saver.filter_vacancies(lambda v: "Java" in v.requirements)
    assert len(filtered) == 1
    assert filtered[0].name == "Java Developer"

def test_load_from_file(temp_file, test_vacancy):
    """Проверка загрузки вакансий из файла"""
    # Очищаем файл перед тестом
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write('[]')
        
    # Сначала сохраняем вакансию
    saver1 = JsonSaver(temp_file)
    saver1.add_vacancy(test_vacancy)
    
    # Затем создаем новый экземпляр и загружаем данные
    saver2 = JsonSaver(temp_file)
    loaded_vacancies = saver2.load_from_file()
    
    assert len(loaded_vacancies) == 1
    assert loaded_vacancies[0].name == test_vacancy.name
    assert loaded_vacancies[0].url == test_vacancy.url

def test_load_invalid_file(tmp_path):
    """Проверка загрузки из несуществующего файла"""
    non_existent_file = tmp_path / "non_existent.json"
    saver = JsonSaver(str(non_existent_file))
    assert saver.load_from_file() == []

def test_file_validation(temp_file):
    """Проверка валидации данных при загрузке из файла"""
    # Создаем файл с некорректными данными
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump([
            {"name": "Valid Vacancy", "url": "https://valid.com"},
            {"invalid": "Missing required fields"}
        ], f)
    
    saver = JsonSaver(temp_file)
    vacancies = saver.load_from_file()
    
    # Должна быть загружена только валидная вакансия
    assert len(vacancies) == 1
    assert vacancies[0].name == "Valid Vacancy"

def test_empty_file(temp_file):
    """Проверка работы с пустым файлом"""
    # Создаем пустой файл
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write('')
    
    saver = JsonSaver(temp_file)
    assert saver.load_from_file() == []
    
    # Добавляем вакансию в пустой файл
    vacancy = Vacancy("Test", "Requirements", "url.com")
    saver.add_vacancy(vacancy)
    
    # Проверяем, что вакансия добавлена
    assert len(saver.vacancies) == 1