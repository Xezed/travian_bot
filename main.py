import os
import requests

from bs4 import BeautifulSoup


SERVER_URL = 'https://ts7.travian.com/'
LOGIN_URL = SERVER_URL + 'dorf1.php'
LOGIN_USERNAME = os.environ['LOGIN_USERNAME']
LOGIN_PASSWORD = os.environ['LOGIN_PASSWORD']


def login(session, url):
    data = {
        'name': LOGIN_USERNAME,
        'password': LOGIN_PASSWORD,
        's1': 'Login',
        'w': '1366:768',
        'login': login
    }

    resp = session.post(url, data=data)
    return resp.text


def parse_field(html):
    parser = BeautifulSoup(html, 'html.parser')
    resource_level = parser.find(class_='level')
    return resource_level


def buildings(session, url):
    resp = session.get(url)
    return resp.text


def main():
    with requests.session() as session:
        html = login(session, LOGIN_URL)
        parser = BeautifulSoup(html, 'html.parser')
        areas = [area.get('href') for area in parser.find_all('area')[:-1]]
        print(areas)


if __name__ == '__main__':
    main()
