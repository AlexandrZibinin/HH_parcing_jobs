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
        """создание курсора"""
        conn = self.connect_db()
        cur = conn.cursor()
        return cur

    def create_database(self, database_name='hhru'):
        """Создание базы данных"""
        cur = self.create_cur()
        try:
            cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
            cur.execute(f'CREATE DATABASE {database_name}')
            print(f'База данных {database_name} очищена и создана повторно')
        except Exception as e:
            print(f'Ошибка при создании базы данных: {e}')

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname='hhru', **self.params)
        with conn.cursor() as cur:
            cur.execute('''select companies.name, COUNT(vacancies.name) AS count_vacancies FROM vacancies 
                            JOIN companies USING (company_id)
                            GROUP BY companies.name''')
            row = cur.fetchall()
        return row

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(dbname='hhru', **self.params)
        with conn.cursor() as cur:
            cur.execute('''SELECT companies.name, vacancies.name, salary_from, salary_to, url from vacancies
                            JOIN companies USING (company_id)''')
            row = cur.fetchall()
        return row

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(dbname='hhru', **self.params)
        with conn.cursor() as cur:
            cur.execute('''SELECT AVG(salary_from) AS avg_salary_from, AVG(salary_to) AS avg_salary_to from vacancies''')
            row = cur.fetchall()
        return row

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname='hhru', **self.params)
        with conn.cursor() as cur:
            cur.execute(
                '''SELECT * FROM vacancies
                    WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies) AND 
                    salary_to > (SELECT AVG(salary_to) FROM vacancies)''')
            row = cur.fetchall()
        return row

    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        user_input = input('Введите слово для поиска: ')
        conn = psycopg2.connect(dbname='hhru', **self.params)
        with conn.cursor() as cur:
            cur.execute('''SELECT * FROM vacancies''')
            row = cur.fetchall()

            result = []
            for vac in row:
                if user_input.lower() in str(vac[2]).lower():
                    result.append(vac)
        return result
