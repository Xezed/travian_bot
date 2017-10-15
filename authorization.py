from credentials import LOGIN_URL, LOGIN_PASSWORD, LOGIN_USERNAME


def login(session):
    data = {
        'name': LOGIN_USERNAME,
        'password': LOGIN_PASSWORD,
        's1': 'Login',
        'w': '1366:768',
        'login': login
    }

    resp = session.post(LOGIN_URL, data=data)
    return resp.text
