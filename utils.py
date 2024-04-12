from typing import Any
import requests
from employees_id import employees_ids

def get_hh_data(employees_ids:dict) -> list[list, Any]:
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
