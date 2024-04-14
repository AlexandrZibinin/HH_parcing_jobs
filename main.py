from utils import config
from utils import get_hh_data
from companies_ids import company_ids
from DBManager import DBManager


def main():
    params = config()
    db_manage = DBManager(params)
    db_manage.connect_db()
    db_manage.create_cur()
    db_manage.create_database()


if __name__ == '__main__':
    main()