import time

import requests

from authorization import login
from credentials import SERVER_URL, HEADERS, VILLAGE_URL
from parse_town_buildings import BuildBuilding
from parse_village_fields import BuildField


def main():
    with requests.Session() as session:
        session.headers = HEADERS
        html = login(session, VILLAGE_URL)

        # buidings_queue = ['Barracks', 'Academy']
        # buidings_queue = ['Main', 'Main', 'Main', 'Main', 'Main']
        # build_building = BuildBuilding(html, session)
        # build_building = build_building()
        # TODO asynchronous queue

        while True:
            build_field = BuildField(html, session)
            seconds_left = build_field()
            print(seconds_left)
            for i in range(seconds_left):
                # In order to take session alive
                time.sleep(1)
                if i % 240 == 0:
                    print('request!')
                    html = session.get(VILLAGE_URL)
            html = session.get(VILLAGE_URL).text


if __name__ == '__main__':
    main()
