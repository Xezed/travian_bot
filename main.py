import asyncio

from building.parse_town_buildings import UpgradeBuilding
from building.parse_village_fields import BuildField
from credentials import VILLAGE_URL, TOWN_URL
from send_troops import TroopsOrder


def builders_manager():
    # Here you can set up your building queue.

    asyncio.async(builder('?newdid=65970&', []))
    asyncio.async(builder('?newdid=57154&', []))


async def builder(village_special_url, buildings_queue):
    if buildings_queue:
        upgrade_building = UpgradeBuilding(TOWN_URL + village_special_url, buildings_queue)
        await upgrade_building()

    build_field = BuildField(VILLAGE_URL + village_special_url)
    await build_field()


# def trooper():
#     with open('raids.txt', 'r') as f:
#
#         for line in f.readlines():
#             coords, time_of_next_raid = line.split(';')
#             coords = eval(coords)
#             asyncio.async(order(coords=coords, time_of_next_raid=time_of_next_raid))
#
#
# async def order(coords=None, time_of_next_raid=None):
#
#     order = TroopsOrder(barrack_url='https://ts7.travian.com/build.php?newdid=57154&id=39&tt=2&gid=16',
#                         coords=coords, time_of_next_raid=time_of_next_raid)
#     await order()


def main():
    builders_manager()
    # trooper()

    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()
