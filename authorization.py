import requests

from bs4 import BeautifulSoup

from credentials import LOGIN_PASSWORD, LOGIN_USERNAME, HEADERS, VILLAGE_URL


def logged_in_session():
    session = requests.Session()
    session.headers = HEADERS
    html = session.get(VILLAGE_URL).text
    resp_parser = BeautifulSoup(html, 'html.parser')
    login_value = resp_parser.find('input', {'name': 'login'})['value']

    data = {
        'name': LOGIN_USERNAME,
        'password': LOGIN_PASSWORD,
        's1': 'Login',
        'w': '1600:900',
        'login': login_value
    }

    session.post(VILLAGE_URL, data=data)

    return session
