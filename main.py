from collections import deque
from random import randint
from time import sleep

from credentials import VILLAGE_URL, TOWN_URL
from parse_town_buildings import UpgradeBuilding
from parse_village_fields import BuildField


def main():
    # TODO asynchronous queue

    buildings_queue = deque(('Main',))
    upgrade_building = UpgradeBuilding(TOWN_URL, buildings_queue)

    while True:
        plus_seconds = randint(10, 90)

        if upgrade_building.queue:
            seconds_left = upgrade_building()
            print(seconds_left)

        else:
            build_field = BuildField(VILLAGE_URL)
            seconds_left = build_field()

        print(seconds_left)
        print('plus seconds {!r}'.format(plus_seconds))
        sleep(seconds_left + plus_seconds)


if __name__ == '__main__':
    main()
