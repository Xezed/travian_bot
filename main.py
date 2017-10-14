import os
import re
import requests
import sys

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


def parse_fields(parser):

    # Last link leads to town, so delete its
    fields = parser.find_all('area')[:-1]

    # Level of buildings and related links in village
    fields = {field.get('alt'): field.get('href') for field in fields}

    return fields


def select_field_to_build(fields, resource):
    """Select field where will be built new resource-field"""
    lowest_level = sys.maxsize
    field_link = None

    for field, link in fields.items():
        fields_level = int(field[-1])

        if (resource in field.lower()) and (fields_level < lowest_level):
            field_link = link

    return SERVER_URL + field_link


def parse_resource(id, parser):
    """Takes id of resource-tag in html and return amount of this resource"""
    pattern = re.compile(r'\d+')

    resource = parser.find(id=id).text
    resource = resource.replace('.', '')

    amount = pattern.search(resource)
    amount = amount.group(0)

    return amount


def parse_resources_amount(parser):
    lumber = parse_resource('l1', parser)
    clay = parse_resource('l2', parser)
    iron = parse_resource('l3', parser)
    crop = parse_resource('l4', parser)

    resources_amount = {'lumber': lumber, 'clay': clay,
                        'iron': iron, 'crop': crop}
    return resources_amount


def main():
    with requests.session() as session:
        html = login(session, LOGIN_URL)
        parser = BeautifulSoup(html, 'html.parser')

        resources_amount = parse_resources_amount(parser)
        minimal_resource = min(resources_amount, key=resources_amount.get)
        fields = parse_fields(parser)

        building_link = select_field_to_build(fields, minimal_resource)

        html = session.get(building_link).text
        parser = BeautifulSoup(html, 'html.parser')

        link_to_upgrade = parser.find_all(class_='green build', value="Upgrade to level 3")[0].get('onclick')

        pattern = re.compile(r'(?<=\').*(?=\')')

        building_link = SERVER_URL + pattern.search(link_to_upgrade).group(0)

        session.get(building_link)


if __name__ == '__main__':
    main()
