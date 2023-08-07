from config import config
from DBManager import DBManager
from utils import formatting_data


def main():
    params = config()
    db = DBManager(dbname='hh_ru', **params)
    db.drop_tables()
    db.create_tables()

    employer_ids = [
        1255642,  # ИТ Альянс
        858127,  # ИТ Синтез
        4934,  # Билайн
        2523,  # М.Видео-Эльдорадо
        6093,  # ИНВИТРО
        11680,  # Дом.РФ
        78638,  # Тинькофф
        1740,  # Яндекс
        3529,  # Сбербанк
        1668887,  # PROF-IT GROUP
    ]
    keyword = input('Введите слово для поиска: ')
    for employer_id in employer_ids:
        url = f'https://api.hh.ru/vacancies?employer_id={employer_id}'
        data = formatting_data(url, keyword)
        db.filling_tables(data)
    while True:
        num = input('''Введите цифру действия:
           (все вакансии сохраняются в файл)
           1. Вывести список всех компаний с количеством вакансий
           2. Вывести список всех вакансий с названием компании, зарплатой и ссылкой
           3. Вывести список всех вакансий со средней зарплатой
           4. Вывести список всех вакансий, у которых зарплата выше средней
           5. Вывести список всех вакансий, в названии которых есть слово поиска
           6. Выход\n''')
        if not num in '123456':
            print('Выберите цифру от 1 до 6')
            continue
        else:
            if num == '1':
                db.get_companies_and_vacancies_count()
            elif num == '2':
                db.get_all_vacancies()
            elif num == '3':
                db.get_avg_salary()
            elif num == '4':
                db.get_vacancies_with_higher_salary()
            elif num == '5':
                user_input = input('Ведите слово поиска:\n')
                result = db.get_vacancies_with_keyword(user_input)
                if not result:
                    print('Такой вакансии не найден')
                    continue
                else:
                    db.get_vacancies_with_keyword(user_input)
            elif num == '6':
                break


if __name__ == '__main__':
    main()
