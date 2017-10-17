import time

import requests

from authorization import login
from credentials import HEADERS, VILLAGE_URL, TOWN_URL
from parse_town_buildings import UpgradeBuilding
from parse_village_fields import BuildField


def main():
    with requests.Session() as session:
        session.headers = HEADERS
        html = login(session, VILLAGE_URL)
        html = session.get(TOWN_URL).text
        with open('1.html', 'w') as f:
            f.write(html)
        buildings_queue = ['Main', 'Main', 'Main', 'Main', 'Main']

        # TODO asynchronous queue

        # while True:
        #     build_field = BuildField(html, session)
        #     seconds_left = build_field()
        #     print(seconds_left)
        #     for i in range(seconds_left):
        #         # In order to take session alive
        #         time.sleep(1)
        #         if i % 240 == 0:
        #             print('{!r} seconds passed'.format(i))
        #             html = session.get(VILLAGE_URL)
        #     html = session.get(VILLAGE_URL).text

        while True:
            build_building = UpgradeBuilding(html, session, buildings_queue)
            seconds_left = build_building()
            print(seconds_left)
            for i in range(seconds_left):
                # In order to take session alive
                time.sleep(1)
                if i % 240 == 0:
                    print('{!r} seconds passed'.format(i))
                    session.get(TOWN_URL)
            html = session.get(TOWN_URL).text


if __name__ == '__main__':
    main()
