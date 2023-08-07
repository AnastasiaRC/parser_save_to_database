import os
import psycopg2


class DBManager:
    def __init__(self, dbname, host, user, password):
        self.conn = psycopg2.connect(dbname=dbname, host=host, user=user, password=password)

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""CREATE TABLE companies(
            company_id SERIAL PRIMARY KEY,
            title_company VARCHAR(255) NOT NULL UNIQUE,
            area VARCHAR(255) NOT NULL);
            CREATE TABLE vacancies(
            vacancy_id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(company_id),
            title_vacancy VARCHAR(255) NOT NULL,
            salary_from INTEGER NOT NULL,
            salary_to INTEGER NOT NULL,
            currency VARCHAR(255) NOT NULL,
            vacancy_url TEXT);
            ALTER TABLE vacancies
            ADD CONSTRAINT fk_vacancies_company_id FOREIGN KEY (company_id) REFERENCES companies ON DELETE CASCADE
            """)
        self.conn.commit()

    def filling_tables(self, data):
        with self.conn.cursor() as cur:
            title_company_save = None
            for row in data:
                if row['title_company'] == title_company_save:
                    pass
                else:
                    cur.execute("""INSERT INTO companies (title_company, area)
                                VALUES (%s, %s) returning company_id""",
                                (row['title_company'], row['area']))
                    title_company_save = row['title_company']
                    company_id = cur.fetchone()[0]
                if company_id == 0:
                    pass
                else:
                    cur.execute("""INSERT INTO vacancies (company_id, title_vacancy, salary_from, salary_to, currency, vacancy_url)
                            VALUES (%s, %s, %s, %s, %s, %s)""",
                                (
                                company_id, row['title_vacancy'], row['salary_from'], row['salary_to'], row['currency'],
                                row['url']))
        self.conn.commit()

    def drop_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE vacancies")
            cur.execute("DROP TABLE companies")
        self.conn.commit()

    def retention_sql_result(self, sql):
        with open(f'{os.path.dirname(os.path.realpath(__file__))}/sql_data.sql', 'a+') as f:
            f.write(sql + '\n')

    def running_query(self, sql):
        with self.conn.cursor() as cur:
            cur.execute(sql)
            all_rows = cur.fetchall()
            for row in all_rows:
                self.retention_sql_result(str(row))
                print(row)

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        sql = """
                SELECT title_company, count(*) AS count_vacancies
                FROM companies 
                INNER JOIN vacancies ON companies.company_id = vacancies.company_id
                GROUP BY vacancies.company_id, companies.title_company
                ORDER BY title_company"""
        return self.running_query(sql)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты
        и ссылки на вакансию."""
        sql = """
                SELECT companies.title_company, title_vacancy, salary_from, salary_to, currency, vacancy_url
                FROM vacancies
                INNER JOIN companies USING(company_id)"""
        return self.running_query(sql)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        sql = """ SELECT title_vacancy, round(avg((salary_from + salary_to) / 2)) AS avg_salary, currency FROM vacancies
                GROUP BY title_vacancy, currency"""
        return self.running_query(sql)

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        sql = """SELECT title_vacancy, round(avg((salary_from + salary_to) / 2)) AS avg_salary, currency FROM vacancies
                GROUP BY title_vacancy, currency
                HAVING round(avg((salary_from + salary_to) / 2)) >(SELECT round(avg((salary_from + salary_to) / 2)) FROM vacancies)"""
        return self.running_query(sql)

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова,
        например “python”."""
        sql = f"""SELECT title_vacancy, salary_from, salary_to, currency FROM vacancies
                WHERE title_vacancy LIKE '%{keyword}%'"""
        return self.running_query(sql)
