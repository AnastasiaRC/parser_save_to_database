import requests


def get_hh_data(url, keyword='python'):
    response = []
    for page in range(10):
        params = {
            'per_page': 50,
            'page': page,
            'keyword': keyword,
            'archive': False,
        }
        response.append(requests.get(url, params=params).json())
    return response


def formatting_data(data, keyword='python'):
    format_vacancies = []
    for vacanci in get_hh_data(data, keyword)[0]['items']:
        if not vacanci['salary']:
            continue
        elif not vacanci['salary']['from']:
            continue
        elif not vacanci['salary']['to']:
            continue
        elif vacanci['salary']['currency'] not in ('RUR', 'RUB'):
            continue
        else:
            format_vacancies.append({
                'title_vacancy': vacanci['name'],  # название вакансии
                'title_company': vacanci['employer']['name'],  # название компании
                'url': vacanci['url'],
                'area': vacanci['area']['name'],
                'salary_from': vacanci['salary']['from'],  # зп от
                'salary_to': vacanci['salary']['to'],  # зп до
                'currency': vacanci['salary']['currency']})  # валюта
    return format_vacancies
