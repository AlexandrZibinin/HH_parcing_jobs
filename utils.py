from typing import Any
import requests
import psycopg2
from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    """парсер параметров для подключения к БД из database.ini"""
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


def get_hh_data(companies_ids: dict) -> list[list, Any]:
    """подключение по API к hh.ru и получение информации о работодателе и вакансиях"""

    data = []
    for company in companies_ids:
        com_data = []

        url = 'https://api.hh.ru/employers/' + companies_ids.get(company)
        response = requests.get(url).json()
        com_data = [int(response["id"]), response["name"]]

        url = response["vacancies_url"]
        response_vacancy = requests.get(url).json()

        data.append({
            'company': com_data,
            'vacancyies': response_vacancy['items']
        })
    print('Подключение успешно. Данные выгружены.')
    return data


def create_tables(params):
    """функция для создания таблиц"""
    with psycopg2.connect(dbname='hhru', **params) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            try:
                cur.execute('''DROP TABLE IF EXISTS companies''')
                cur.execute('''DROP TABLE IF EXISTS vacancies''')
                cur.execute('''CREATE TABLE companies 
                                (
                                company_id INTEGER PRIMARY KEY,
                                name VARCHAR(50) NOT NULL
                                )
                                ''')
                cur.execute('''CREATE TABLE vacancies 
                                (
                                vacancy_id INT PRIMARY KEY,
                                company_id INT REFERENCES companies(company_id),
                                name VARCHAR(100) NOT NULL,
                                salary_from INTEGER,
                                salary_to INTEGER,
                                url TEXT
                                )
                                ''')
                print('Таблицы созданы')
            except Exception:
                print('Ошибка при создании таблиц')


def save_data(params, data):
    """функция для сохранения данных в таблицу"""
    conn = psycopg2.connect(dbname='hhru', **params)
    with conn.cursor() as cur:
        for one in data:
            company_data = one['company']
            vacancy_data = one['vacancyies']

            cur.execute('''INSERT INTO companies (company_id, name) VALUES (%s, %s)''',
                        (company_data[0], company_data[1]))

            for vacan in vacancy_data:
                try:
                    cur.execute(
                        '''INSERT INTO vacancies (vacancy_id, company_id, name, salary_from, salary_to, url) VALUES (
                        %s, %s, %s, %s, %s, %s)''',
                        (int(vacan['id']), company_data[0], vacan['name'], vacan['salary']['from'],
                         vacan['salary']['to'], vacan['alternate_url']))
                except Exception:
                    continue

        conn.commit()
    print('Данные успешно сохранены в БД')
