from utils import config, create_tables
from utils import get_hh_data
from companies_ids import company_ids
from DBManager import DBManager
from utils import save_data


def main():
    """подклчюение к БД и создание таблиц"""
    params = config()
    # db_manage = DBManager(params)
    # db_manage.create_database()
    # create_tables(params)

    """подключение по API  к hh.ru и получение данных"""
    data = get_hh_data(company_ids)


    """сохранение данных в БД"""
    save_data(params, data)









if __name__ == '__main__':
    main()