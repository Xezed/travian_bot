import os
import re
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


def parse_resouce(id, parser):
    """Takes id of resource-tag in html and return amount of this resource"""
    pattern = re.compile(r'\d+')

    resource = parser.find(id=id).text
    resource = resource.replace('.', '')

    amount = pattern.search(resource)
    amount = amount.group(0)

    return amount


def parse_resources_amount(parser):
    lumber = parse_resouce('l1', parser)
    clay = parse_resouce('l2', parser)
    iron = parse_resouce('l3', parser)
    crop = parse_resouce('l4', parser)

    resources_amount = {'lumber': lumber, 'clay': clay,
                        'iron': iron, 'crop': crop}
    return resources_amount


def main():
    with requests.session() as session:
        html = login(session, LOGIN_URL)
        parser = BeautifulSoup(html, 'html.parser')

        resources_amount = parse_resources_amount(parser)
        minimal_resource = min(resources_amount, key=resources_amount.get)


if __name__ == '__main__':
    main()
