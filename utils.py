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

def get_hh_data(employees_ids: dict) -> list[list, Any]:
    """подключение по API к hh.ru и получение информации о работодателе и вакансиях"""

    data = []
    for employee in employees_ids:
        emp_data = []

        url = 'https://api.hh.ru/employers/' + employees_ids.get(employee)
        response = requests.get(url).json()
        emp_data.append([response["id"], response["name"]])

        url = response["vacancies_url"]
        response_vacancy = requests.get(url).json()

        data.append({
            'employee': emp_data,
            'vacancyies': response_vacancy['items']
        })

    return data

    with psycopg2.connect(dbname=database_name, **params) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute('''CREATE TABLE companies 
                            (
                            company_id INTEGER PRIMARY KEY,
                            name VARCHAR(50) NOT NULL
                            )
                            ''')
            cur.execute('''CREATE TABLE vacancies 
                            (
                            vacancy_id SERIAL PRIMARY KEY,
                            company_id INT REFERENCES companies(company_id),
                            name VARCHAR(100) NOT NULL,
                            salary_from INTEGER,
                            salary_to INTEGER,
                            url TEXT
                            )
                            ''')
            print('Таблицы созданы')


