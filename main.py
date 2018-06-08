import asyncio
import os

from building.parse_town_buildings import UpgradeBuilding
from building.parse_village_fields import BuildField
from credentials import VILLAGE_URL, TOWN_URL
from send_troops import TroopsOrder


def builders_manager():

    # for the first iteration in a while loop
    village_number = 1
    village_url = os.environ[f'VILLAGE_URL_{village_number}']
    buildings_queue = os.environ[f'BUILDINGS_QUEUE_{village_number}']

    # while village_url is not None
    while village_url:

        buildings_queue = buildings_queue.split()
        asyncio.async(builder(village_url, buildings_queue))

        village_number += 1

        village_url = os.environ.get(f'VILLAGE_URL_{village_number}')
        buildings_queue = os.environ.get(f'BUILDINGS_QUEUE_{village_number}')


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
