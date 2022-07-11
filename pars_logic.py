import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_info():
    """Функция для парсинга информации о городах из википедии"""
    city_info = {}
    ua = UserAgent().random
    data = requests.get(url='https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B8%D0%B5_%D0'
                            '%BD%D0%B0%D1%81%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B5_%D0%BF%D1%83%D0%BD%D0%BA%D1%82'
                            '%D1%8B_%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B9_%D0%BE%D0%B1%D0%BB'
                            '%D0%B0%D1%81%D1%82%D0%B8', headers={'user-agent': ua})
    soap = BeautifulSoup(data.content, 'lxml')
    tables = soap.find_all('table')
    for table in tables[:2]:
        lines = table.find_all('tr')[1:]
        for line in lines:
            city_name = line.find_all('td')[1].find('a').get('title')
            city_population = line.find_all('td')[4].get('data-sort-value')
            city_url = 'https://ru.wikipedia.org' + line.find_all('td')[1].find('a').get('href')
            city_info[city_name] = (city_population, city_url)
    return city_info
