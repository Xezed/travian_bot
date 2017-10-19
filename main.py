from collections import deque

from credentials import VILLAGE_URL, TOWN_URL
from parse_town_buildings import UpgradeBuilding
from parse_village_fields import BuildField


def main():
    # TODO asynchronous queue

    buildings_queue = deque(())
    upgrade_building = UpgradeBuilding(TOWN_URL, buildings_queue)

    while True:
        if upgrade_building.queue:
            upgrade_building()

        else:
            build_field = BuildField(VILLAGE_URL)
            build_field()


if __name__ == '__main__':
    main()
