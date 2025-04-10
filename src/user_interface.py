from file_worker import JsonSaver


def show_vacancies_from_file(filename: str):
    """Отображает вакансии из JSON-файла"""
    saver = JsonSaver(filename)
    vacancies = saver.load_from_file()
    
    if not vacancies:
        print("\n\u001b[31mФайл не содержит валидных вакансий\u001b[0m")
        return
    
    # Выводим информацию о количестве найденных вакансий в формате, ожидаемом в тесте
    print(f"Найдено {len(vacancies)} вакансий")
    
    for vac in vacancies:
        salary = (f"{vac.salary.get('from', '')}-{vac.salary.get('to', '')} {vac.salary.get('currency', '')}" 
                if vac.salary and isinstance(vac.salary, dict) 
                else "не указана")
        print(f"{vac.name}\nЗарплата: {salary}\nРаботодатель: {vac.employer}\nТребования: {vac.requirements}\nСсылка: {vac.url}\n\n{'='*50}\n")


def get_vacancies_by_salary(vacancies, salary_range):
    """Фильтрует вакансии по диапазону зарплат.
    
    Args:
        vacancies (list): Список вакансий
        salary_range (str): Строка с диапазоном зарплат в формате 'min-max'
        
    Returns:
        list: Отфильтрованный список вакансий
    """
    if not salary_range:
        return vacancies
    try:
        min_s, max_s = map(int, salary_range.replace(' ', '').split('-'))
        # Фильтруем вакансии по диапазону зарплат
        # Вакансия подходит, если её минимальная зарплата (from) находится в указанном диапазоне
        return [v for v in vacancies if 
                (v.salary and isinstance(v.salary, dict) and 
                 v.salary.get('from') is not None and 
                 min_s <= v.salary.get('from') <= max_s)]
    except:
        # В случае некорректного формата возвращаем все вакансии
        return vacancies

def sort_vacancies(vacancies):
    """Сортирует вакансии по убыванию зарплаты.
    
    Args:
        vacancies (list): Список вакансий
        
    Returns:
        list: Отсортированный список вакансий
    """
    # Сортируем по максимальному значению зарплаты (to) или по минимальному (from), если to не указано
    def get_salary_for_sort(vacancy):
        if not vacancy.salary or not isinstance(vacancy.salary, dict):
            return 0
        # Если указано максимальное значение зарплаты, используем его
        if vacancy.salary.get('to'):
            return vacancy.salary.get('to')
        # Иначе используем минимальное значение
        return vacancy.salary.get('from', 0) or 0
        
    return sorted(vacancies, key=get_salary_for_sort, reverse=True)

def print_vacancies(vacancies):
    """Выводит информацию о вакансиях в консоль.

    Args:
        vacancies (list[Vacancy]): Список вакансий для вывода

    Returns:
        None
    """
    for vac in vacancies:
        salary = f"{vac.salary['from']}-{vac.salary['to']} {vac.salary['currency']}" if isinstance(vac.salary, dict) and vac.salary else "не указана"
        print(f"{vac.name}\nЗарплата: {salary}\nРаботодатель: {vac.employer}\nТребования: {vac.requirements}\nСсылка: {vac.url}\n\n{'='*50}\n")


def user_interaction():
    json_saver = JsonSaver('vacancies.json')
    
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода: "))
    filter_words = input("Введите ключевые слова через пробел: ").split()
    salary_range = input("Введите диапазон зарплат (пример: 100000-150000): ")

    # Фильтрация и сортировка
    filtered = json_saver.filter_vacancies(lambda v: any(word in v.description for word in filter_words))
    ranged = get_vacancies_by_salary(filtered, salary_range)
    sorted_vacs = sort_vacancies(ranged)
    
    print_vacancies(sorted_vacs[:top_n])