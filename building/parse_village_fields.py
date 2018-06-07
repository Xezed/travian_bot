import sys

from asyncio import sleep

from bs4 import BeautifulSoup

from .builder import Builder
from credentials import SERVER_URL
from logger import get_logger


logger = get_logger(__name__)


class BuildField(Builder):
    """Build field in village. Type depend on minimum resource"""
    def __init__(self, village_page_url):
        super().__init__(village_page_url)

    async def __call__(self, *args, **kwargs):
        successfully_built = await super().__call__()

        if successfully_built:
            await self.__call__()

    def set_parser_location_to_build(self):
        """Return link to field where will be built new resource field"""

        minimal_resource = self.minimal_resource()
        field_link = self.link_to_field_to_build(minimal_resource)

        # If there are some field <10lvl then return link to it. Logged error and sleep otherwise.
        if field_link:
            full_field_link = SERVER_URL + field_link
            field_page = self.session.get(full_field_link).text

            self.parser_location_to_build = BeautifulSoup(field_page, 'html.parser')

            if self.is_enough_crop():
                return

            else:
                field_link = self.link_to_field_to_build('crop')
                full_field_link = SERVER_URL + field_link
                field_page = self.session.get(full_field_link).text
                self.parser_location_to_build = BeautifulSoup(field_page, 'html.parser')
        else:
            logger.error('Some field reached max level!')
            sleep(6000)

    def minimal_resource(self):
        """Return minimal resource"""
        resources_amount = self.parse_resources_amount()
        minimal_resource = min(resources_amount, key=resources_amount.get)

        # In fields it's called wood instead lumber
        if minimal_resource == 'lumber':
            minimal_resource = 'wood'

        return minimal_resource

    def parse_fields(self):
        """Return dictionary with names of fields and appropriate links"""
        # Last link leads to town, so delete its
        fields = self.parser_main_page.find_all('area')[:-1]

        # Level of buildings and related links in village
        fields = {field.get('alt'): field.get('href') for field in fields}

        return fields

    def link_to_field_to_build(self, minimal_resource):
        """Find link to field with minimal resource"""

        fields = self.parse_fields()
        field_link = None
        lowest_level = sys.maxsize

        for field, link in fields.items():
            fields_level = int(field[-1])
            if (minimal_resource in field.lower()) and (10 >= fields_level < lowest_level):
                lowest_level = fields_level
                field_link = link

        return field_link
