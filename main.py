from utils import create_database, config
from utils import get_hh_data
from companies_ids import company_ids


def main():
    params = config()

    create_database('hhru', params)


if __name__ == '__main__':
    main()