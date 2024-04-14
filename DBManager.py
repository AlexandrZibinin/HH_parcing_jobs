import psycopg2

class DBManager:
    def __init__(self, params):
        self.params = params

    def connect_db(self, database_name='hhru'):
        """подключение к БД"""
        with psycopg2.connect(**self.params) as conn:
            conn.autocommit = True
            return conn

    def create_cur(self):
        conn = self.connect_db()
        cur = conn.cursor()
        return cur

    def create_database(self, database_name='hhru'):
        """Создание базы данных и таблиц"""
        conn = self.connect_db()
        cur = self.create_cur()
        try:
            cur.execute(f'DROP DATABASE {database_name}')
        except:
            cur.execute(f'CREATE DATABASE {database_name}')
            print(f'Создание новой базы данных {database_name}')
        else:
            cur.execute(f'CREATE DATABASE {database_name}')
            print(f'База данных {database_name} очищена и создана повторно')
        conn.commit()

    def create_table(self):
        # with psycopg2.connect(self.database_name, **self.params) as conn:
        #     conn.autocommit = True
        #     with conn.cursor() as cur:
        conn = self.connect_db()
        cur = self.create_cur()
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

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        pass

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        pass

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        pass

    def close_db(self):
        """отключение от БД"""
        conn = self.connect_db()
        conn.close()