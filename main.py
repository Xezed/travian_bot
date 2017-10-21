from building.parse_town_buildings import UpgradeBuilding
from building.parse_village_fields import BuildField
from credentials import VILLAGE_URL, TOWN_URL


def main():
    # TODO asynchronous queue

    # Here you can set up your building queue.
    buildings_queue = ['Cranny', 'Cranny']

    if buildings_queue:
        upgrade_building = UpgradeBuilding(TOWN_URL, buildings_queue)
        upgrade_building()

    build_field = BuildField(VILLAGE_URL)
    build_field()


if __name__ == '__main__':
    main()
