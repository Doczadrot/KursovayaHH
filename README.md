# Проект по поиску вакансий на HeadHunter

## Описание проекта

Данный проект представляет собой приложение для поиска и фильтрации вакансий с сайта HeadHunter. Приложение позволяет пользователям искать вакансии по ключевым словам, фильтровать их по зарплате и требованиям, а также сохранять результаты в JSON-файл для дальнейшего использования.

## Функциональные возможности

- Поиск вакансий по ключевым словам через API HeadHunter
- Фильтрация вакансий по диапазону зарплат
- Фильтрация вакансий по ключевым словам в требованиях
- Сортировка вакансий по уровню зарплаты
- Сохранение найденных вакансий в JSON-файл
- Загрузка вакансий из JSON-файла
- Вывод топ-N вакансий по заданным критериям

## Структура проекта

- `src/api.py` - Модуль для работы с API HeadHunter
- `src/vacancy.py` - Класс для представления вакансий
- `src/file_worker.py` - Классы для работы с файлами (сохранение и загрузка вакансий)
- `src/hh.py` - Парсер вакансий с HeadHunter
- `src/user_interface.py` - Функции для взаимодействия с пользователем
- `src/utils.py` - Вспомогательные функции для обработки вакансий
- `main.py` - Основной файл для запуска приложения

## Основные классы

### ApiConnector и HeadHunterApi

Абстрактный класс `ApiConnector` и его реализация `HeadHunterApi` отвечают за подключение к API HeadHunter и получение вакансий.

### Vacancy

Класс `Vacancy` представляет собой модель вакансии с такими атрибутами, как название, требования, URL, зарплата и работодатель.

### Saver и JsonSaver

Абстрактный класс `Saver` и его реализация `JsonSaver` отвечают за сохранение и загрузку вакансий в/из JSON-файла.

### Parser и HH

Абстрактный класс `Parser` и его реализация `HH` отвечают за парсинг вакансий с HeadHunter.

## Технологии

- Python 3
- Библиотека requests для работы с API
- JSON для хранения данных

## Установка и запуск

1. Клонируйте репозиторий:
   ```
   git clone <URL репозитория>
   ```

2. Перейдите в директорию проекта:
   ```
   cd Kursovaya_HH
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Запустите приложение:
   ```
   python main.py
   ```

## Использование

После запуска приложения вам будет предложено:

1. Ввести количество вакансий для вывода в топ N
2. Ввести ключевые слова для фильтрации вакансий
3. Ввести диапазон зарплат (например, "100000-150000")
4. Ввести поисковый запрос для поиска вакансий

После этого приложение выполнит поиск вакансий, применит фильтры и выведет результаты на экран.

## Тестирование

Проект включает набор тестов для проверки функциональности. Для запуска тестов используйте команду:

```
pytest
```

