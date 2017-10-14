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


def parse_field(parser):

    # Last link leads to town, so delete its
    areas = parser.find_all('area')[:-1]

    # Level of buildings and related links in village
    areas = {area.get('alt'): area.get('href') for area in areas}

    return areas

def parse_resources_amount(parser):
    lumber = parser.find(id='stockBarResource1')
    clay = parser.find(id='stockBarResource2')
    iron = parser.find(id='stockBarResource3')
    crop = parser.find(id='stockBarResource4')

    resources_amount = {'lumber': lumber, 'clay': clay,
                        'iron': iron, 'crop': crop}
    return resources_amount


def buildings(session, url):
    resp = session.get(url)
    return resp.text


def main():
    with requests.session() as session:
        html = login(session, LOGIN_URL)
        parser = BeautifulSoup(html, 'html.parser')



        print(areas)


if __name__ == '__main__':
    main()
