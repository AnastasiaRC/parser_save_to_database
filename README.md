# Работа с базами данных

<aside>
🧑🏻‍💻 В рамках проекта получаем данные о компаниях и вакансиях с сайта [hh.ru](http://hh.ru/)
   Создаем таблицы в БД PostgreSQL и загружаем полученные данные в созданные таблицы.

</aside>

## Основные шаги проекта

- Получаем данные о работодателях и их вакансиях с сайта [hh.ru](http://hh.ru/). Для этого используется публичный API [hh.ru](http://hh.ru/) и библиотека `requests`.
- Выбирается не менее 10 интересных компаний, от которых получаем данные о вакансиях по API.
- Проектируем таблицы в БД Postgres для хранения полученных данных о работодателях и их вакансиях. Для работы с БД используется библиотека `psycopg2`.
- Реализован код, который заполняет созданные таблицы в БД Postgres данными о работодателях и их вакансиях.
- Создан класс `DBManager` для работы с данными в БД.

## Класс DBManager

Класс `DBManager`, который подключаться к БД Postgres и иметь следующие методы:

- `get_companies_and_vacancies_count()`: получает список всех компаний и количество вакансий у каждой компании.
- `get_all_vacancies()`: получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
- `get_avg_salary()`: получает среднюю зарплату по вакансиям.
- `get_vacancies_with_higher_salary()`: получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
- `get_vacancies_with_keyword()`: получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
