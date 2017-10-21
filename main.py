import asyncio

from building.parse_town_buildings import UpgradeBuilding
from building.parse_village_fields import BuildField
from credentials import VILLAGE_URL, TOWN_URL


async def builder():
    # Here you can set up your building queue.
    buildings_queue = []

    if buildings_queue:
        upgrade_building = UpgradeBuilding(TOWN_URL, buildings_queue)
        await upgrade_building()

    build_field = BuildField(VILLAGE_URL)
    await build_field()


def main():
    # TODO asynchronous queue
    loop = asyncio.get_event_loop()
    loop.run_until_complete(builder())


if __name__ == '__main__':
    main()
