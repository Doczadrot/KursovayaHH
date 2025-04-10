from src.api import HeadHunterApi
from src.file_worker import JsonSaver
from src.vacancy import Vacancy

hh_api = HeadHunterApi()
json_saver = JsonSaver('vacancies.json')


def user_interaction():
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000
    search_query = input("Введите поисковый запрос: ")
    hh_vacancies = hh_api.get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    for vacancy in vacancies_list:
        try:
            json_saver.add_vacancy(vacancy)
        except ValueError as e:
            # Пропускаем существующие вакансии
            pass
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)

def filter_vacancies(vacancies_list, filter_words):
    """Фильтрует вакансии по ключевым словам в требованиях
    
    Args:
        vacancies_list (list): Список вакансий
        filter_words (list): Список ключевых слов для фильтрации
        
    Returns:
        list: Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies_list
    
    # Проверяем, что requirements не None перед вызовом lower()
    return [v for v in vacancies_list if v.requirements is not None and any(word.lower() in v.requirements.lower() for word in filter_words)]


def get_vacancies_by_salary(vacancies, salary_range):
    """Фильтрует вакансии по диапазону зарплат
    
    Args:
        vacancies (list): Список вакансий
        salary_range (str): Строка с диапазоном зарплат (например, "100000-150000")
        
    Returns:
        list: Отфильтрованный список вакансий
    """
    if not salary_range:
        return vacancies
    try:
        min_s, max_s = map(int, salary_range.replace(' ', '').split('-'))
        # Фильтруем вакансии, у которых минимальная зарплата попадает в указанный диапазон
        return [v for v in vacancies if min_s <= v.get_min_salary() <= max_s]
    except:
        return vacancies


def sort_vacancies(vacancies_list):
    """Сортирует вакансии по зарплате (по убыванию)
    
    Args:
        vacancies_list (list): Список вакансий
        
    Returns:
        list: Отсортированный список вакансий
    """
    return sorted(vacancies_list, reverse=True)


def get_top_vacancies(vacancies_list, top_n):
    """Возвращает top_n вакансий из списка
    
    Args:
        vacancies_list (list): Список вакансий
        top_n (int): Количество вакансий для вывода
        
    Returns:
        list: Список top_n вакансий
    """
    return vacancies_list[:top_n]


def print_vacancies(vacancies):
    """Выводит информацию о вакансиях
    
    Args:
        vacancies (list): Список вакансий для вывода
    """
    if not vacancies:
        print("\nНет вакансий, соответствующих заданным критериям")
        return
        
    print(f"\nНайдено {len(vacancies)} вакансий:")
    for vac in vacancies:
        salary = "не указана"
        if vac.salary:
            from_val = vac.salary.get('from', '')
            to_val = vac.salary.get('to', '')
            currency = vac.salary.get('currency', '')
            
            if from_val and to_val:
                salary = f"{from_val}-{to_val} {currency}"
            elif from_val:
                salary = f"от {from_val} {currency}"
            elif to_val:
                salary = f"до {to_val} {currency}"
                
        print(f"\n• {vac.name}\n  Зарплата: {salary}\n  Работодатель: {vac.employer}\n  Ссылка: {vac.url}")

