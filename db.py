import psycopg2

def insert_vacancies_to_db(vacancies, keyword):
    conn = psycopg2.connect(
        dbname='hh_parsing',
        user='postgres',
        password='dashka335',
        host='db',
        port='5432'
    )
    cur = conn.cursor()

    # Создание таблицы vacancies, если она не существует
    cur.execute('''
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        keyword TEXT,
        company TEXT,
        city TEXT,
        salary TEXT,
        url TEXT
    )
    ''')
    conn.commit()

    # Внесение данных о вакансиях в базу данных
    for vacancy in vacancies:
        # Преобразование salary в строку
        salary_info = vacancy['salary']
        if isinstance(salary_info, dict):
            salary_str = f"{salary_info.get('from', 'Не указано')} - {salary_info.get('to', 'Не указано')} {salary_info.get('currency', 'Не указано')}"
        elif salary_info is None or salary_info == 'Зарплата не указана':
            salary_str = 'Зарплата не указана'
        else:
            salary_str = str(salary_info)

        cur.execute('''
            INSERT INTO vacancies (keyword, company, city, salary, url)
            VALUES (%s, %s, %s, %s, %s)
        ''', (keyword, vacancy['company'], vacancy['city'], salary_str, vacancy['url']))
    conn.commit()

    # Закрытие курсора и соединения с базой данных
    cur.close()
    conn.close()


