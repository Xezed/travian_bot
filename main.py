import asyncio

from building.parse_town_buildings import UpgradeBuilding
from building.parse_village_fields import BuildField
from credentials import VILLAGE_URL, TOWN_URL
from send_troops import TroopsOrder


async def builder():
    # Here you can set up your building queue.
    buildings_queue = []

    if buildings_queue:
        upgrade_building = UpgradeBuilding(TOWN_URL, buildings_queue)
        await upgrade_building()

    build_field = BuildField(VILLAGE_URL)
    await build_field()


# async def trooper():
#     order = TroopsOrder(barrack_url='https://ts7.travian.com/build.php?tt=2&id=39')


def main():
    asyncio.async(builder())

    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()
