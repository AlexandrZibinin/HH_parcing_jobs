from utils import config, create_tables
from utils import get_hh_data
from companies_ids import company_ids
from DBManager import DBManager
from utils import save_data

def main():
    """подключение к БД и создание таблиц"""
    params = config()
    db_manage = DBManager(params)
    db_manage.create_database()
    create_tables(params)

    """подключение по API  к hh.ru и получение данных"""
    data = get_hh_data(company_ids)

    """сохранение данных в БД"""
    save_data(params, data)

    """интерактив с пользователем"""
    while True:
        user_input = input("""Выберете команду:
     [1] - список всех компаний и количество их вакансий.
     [2] - список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
     [3] - средняя зарплата по вакансиям.
     [4] - список всех вакансий, у которых зарплата выше средней по всем вакансиям.
     [5] - список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
     [0] - выход.\n:""")
        match user_input:

            case '1':
                data = db_manage.get_companies_and_vacancies_count()
                for one in data:
                    print(*one)
                continue
            case '2':
                data = db_manage.get_all_vacancies()
                for one in data:
                    print(*one)
                continue
            case '3':
                data = db_manage.get_avg_salary()
                for one in data:
                    print(*one)
                continue
            case '4':
                data = db_manage.get_vacancies_with_higher_salary()
                for one in data:
                    print(*one)
                continue
            case '5':
                data = db_manage.get_vacancies_with_keyword()
                for one in data:
                    print(*one)
                continue
            case '0':
                print('Программа завершена.')
                break


if __name__ == '__main__':
    main()