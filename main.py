import requests
import time

from authorization import login, LOGIN_URL
from credentials import SERVER_URL
from parse_town_buildings import BuildBuilding
from parse_village_fields import BuildField


def main():
    with requests.Session() as session:
        html = login(session)
        html = session.get(SERVER_URL + 'dorf2.php').text
        with open('1.html', 'w') as f:
            f.write(html)
        build_building = BuildBuilding(html, session)
        build_building = build_building.parse_buildings()
        # TODO asynchronous queue

        # while True:
        #     build_field = BuildField(html, session)
        #     seconds_left = build_field.build_field()
        #     print(seconds_left)
        #     for i in range(seconds_left):
        #         # In order to take session alive
        #         time.sleep(1)
        #         if i % 100 == 0:
        #             print('request!')
        #             html = session.get(LOGIN_URL)
        #     html = session.get(LOGIN_URL).text


if __name__ == '__main__':
    main()
