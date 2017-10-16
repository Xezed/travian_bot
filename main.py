import requests
import time

from authorization import login, LOGIN_URL
from parse_village_fields import BuildField


def main():
    with requests.Session() as session:
        html = login(session)
        # TODO asynchronous queue
        while True:
            build_field = BuildField(html, session)
            seconds_left = build_field.build_field()
            print(seconds_left)
            for i in range(seconds_left):
                # In order to take session alive
                time.sleep(1)
                if i % 100 == 0:
                    print('request!')
                    html = session.get(LOGIN_URL)
            html = session.get(LOGIN_URL).text


if __name__ == '__main__':
    main()
