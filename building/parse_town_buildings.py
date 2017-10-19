import re
from collections import deque

from .builder import Builder
from credentials import SERVER_URL


class UpgradeBuilding(Builder):
    """Build the list of buildings"""
    def __init__(self, town_page_url, queue):
        super().__init__(town_page_url)
        self.queue = deque(queue)

    def parse_buildings(self):
        """Return all buildings and related links"""

        buildings = self.parser_main_page.find_all('area')
        building_links = {}

        for building in buildings:
            alt_attr = building.get('alt')
            first_word = re.match(r'^\w+', alt_attr).group(0)
            link = building.get('href')
            building_links[first_word] = link

        return building_links

    def link_on_location_to_build(self):
        building_to_build = self.queue.popleft()
        building_sites = self.parse_buildings()

        # If given building was found then return link to it, else KeyError.
        if building_to_build in building_sites:
            return SERVER_URL + building_sites[building_to_build]

        else:
            raise KeyError('Incorrect input of building name')





