import psycopg2
from pars_logic import get_info
import config


def connection():
    """Функция подключения к БД"""
    connect = psycopg2.connect(database='bot_alef_db',
                               user='postgres',
                               password=config.DB_PASS,
                               host='127.0.0.1',
                               port='5432')
    return connect


def insert_update_data():
    """Функция для записи информации из википедии в БД"""
    parsed_data = get_info()
    connect = connection()
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM cities_info")
    rows = cursor.fetchall()
    if not rows:
        for key, value in parsed_data.items():
            cursor.execute('INSERT INTO cities_info (city_name, city_population, city_url) VALUES (%s, %s, %s)',
                           (key, value[0], value[1]))
            connect.commit()
    else:
        for row in rows:
            if parsed_data.get(row[0]) != (row[1], row[2]):
                cursor.execute('UPDATE cities_info set city_population=%s, city_url=%s where city_name=%s',
                               (parsed_data.get(row[0])[0], parsed_data.get(row[0])[1], row[0]))
                connect.commit()
    connect.close()


def get_data(message):
    """Функция получения данных из БД"""
    connect = connection()
    cursor = connect.cursor()
    cursor.execute('SELECT city_name FROM cities_info')
    cities = cursor.fetchall()
    city_name = list(filter(lambda x: x.lower() == message.lower(), map(lambda y: y[0], cities)))
    if city_name:
        cursor.execute("SELECT city_name, city_population, city_url FROM cities_info WHERE city_name=%s",
                       (city_name[0],))
        city_info = cursor.fetchone()
        answer = f'Город: {city_info[0]} имеет население {city_info[1]} человек. Ссылка на вики: {city_info[2]}'
    else:
        cursor.execute(f"SELECT city_name FROM cities_info WHERE city_name ILIKE '%{message}%'")
        city_info = cursor.fetchall()
        if city_info:
            answer = 'Возможно Вы имели ввиду один из этих городов: ' + ', '.join([str(i[0]) for i in city_info])
        else:
            answer = 'Такого города нет!!!'
    connect.close()
    return answer
