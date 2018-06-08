import re

from bs4 import BeautifulSoup

from .builder import Builder
from credentials import SERVER_URL


class UpgradeBuilding(Builder):
    """Build the list of buildings"""
    def __init__(self, town_page_url, queue):
        super().__init__(town_page_url)
        self.queue = list(queue)

    async def __call__(self, *args, **kwargs):
        """Build buildings until queue is not empty."""
        if self.queue:
            successfully_built = await super().__call__(*args, **kwargs)

            if successfully_built:
                del self.queue[0]

            await self.__call__()

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

    def set_parser_location_to_build(self):
        building_to_build = self.queue[0]
        building_sites = self.parse_buildings()

        # If given building was found then set parser, else KeyError.
        if building_to_build in building_sites:
            link_to_building_field = SERVER_URL + building_sites[building_to_build]
            building_field_page = self.session.get(link_to_building_field).text

            self.parser_location_to_build = BeautifulSoup(building_field_page, 'html.parser')

        else:
            raise KeyError(f'Incorrect input of building name {building_to_build}')
