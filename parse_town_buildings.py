import re

from collections import deque

from builder import Builder
from credentials import SERVER_URL


class BuildBuilding(Builder):
    """Build the list of buildings"""
    def __init__(self, html, session, queue):
        super().__init__(html, session)
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
        building_to_build = deque.popleft()
        building_sites = self.parse_buildings()

        if building_to_build in building_sites:
            return SERVER_URL + building_sites[building_to_build]

        else:
            # TODO building is not exist, need to build a new one
            pass

        raise KeyError('Incorrect input of building name')





