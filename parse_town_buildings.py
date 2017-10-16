import re

from bs4 import BeautifulSoup


class BuildBuilding:
    """Build the list of buildings"""
    def __init__(self, html, session):
        self.parser_town_page = BeautifulSoup(html, 'html.parser')
        self.session = session
        # self.queue = queue

    def parse_buildings(self):
        """Return all buildings and related links"""
        buildings = self.parser_town_page.find_all('area')

        building_links = {}

        for building in buildings:
            alt_attr = building.get('alt')
            first_word = re.match(r'^\w+', alt_attr).group(0)
            link = building.get('href')
            building_links[first_word] = link

        print(building_links)
