from bs4 import BeautifulSoup

from credentials import LOGIN_PASSWORD, LOGIN_USERNAME


def login(session=None, url=None):
    html = session.get(url).text
    resp_parser = BeautifulSoup(html, 'html.parser')
    login_value = resp_parser.find('input', {'name': 'login'})['value']
    print(login_value)

    data = {
        'name': LOGIN_USERNAME,
        'password': LOGIN_PASSWORD,
        's1': 'Login',
        'w': '1600:900',
        'login': login_value
    }

    html = session.post(url, data=data).text

    return html
