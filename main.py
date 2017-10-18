from time import sleep

import requests

from adventure_check import adventure_check
from authorization import login
from credentials import HEADERS, VILLAGE_URL, TOWN_URL
from parse_town_buildings import UpgradeBuilding
from parse_village_fields import BuildField


def main():
    # with requests.Session() as session:

    # with open('1.html', 'w') as f:
    #     f.write(html)
    # buildings_queue = ['Main', 'Main', 'Main']

    # TODO asynchronous queue

    while True:
        session = requests.Session()
        session.headers = HEADERS
        html = login(session, VILLAGE_URL)
        html = session.get(VILLAGE_URL).text
        build_field = BuildField(html, session)
        seconds_left = build_field()
        print(seconds_left)
        adventure_check(html, session)
        sleep(seconds_left)
        print('Sleep...')

    # build_building = UpgradeBuilding(html, session, buildings_queue)
    # while True:
    #     seconds_left = build_building()
    #     print(seconds_left)
    #     for i in range(seconds_left):
    #         # In order to take session alive
    #         time.sleep(1)
    #         if i % 240 == 0:
    #             print('{!r} seconds passed'.format(i))
    #             html = session.get(TOWN_URL).text
    #             adventure_check(html, session)
    #     html = session.get(TOWN_URL).text
    #     build_building.html = html


if __name__ == '__main__':
    main()
