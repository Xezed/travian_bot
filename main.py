from building.parse_town_buildings import UpgradeBuilding
from building.parse_village_fields import BuildField
from credentials import VILLAGE_URL, TOWN_URL


def main():
    # TODO asynchronous queue

    # Here you can set up your building queue.
    buildings_queue = []

    build_field = BuildField(VILLAGE_URL)
    upgrade_building = UpgradeBuilding(TOWN_URL, buildings_queue)

    while True:
        if upgrade_building.queue:
            upgrade_building()

        else:
            build_field()


if __name__ == '__main__':
    main()
