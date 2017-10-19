import sys

from .builder import Builder
from credentials import SERVER_URL


class BuildField(Builder):
    """Build field in village. Type depend on minimum resource"""
    def __init__(self, village_page_url):
        super().__init__(village_page_url)

    def link_on_location_to_build(self):
        """Return link to field where will be built new resource field"""

        field_link = None
        fields = self.parse_fields()
        lowest_level = sys.maxsize
        minimal_resource = self.minimal_resource()

        # find link to field with minimal resource
        for field, link in fields.items():
            fields_level = int(field[-1])
            if (minimal_resource in field.lower()) and (fields_level < lowest_level):
                lowest_level = fields_level
                field_link = link

        return SERVER_URL + field_link

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

        # Temporary for the quest
        del fields[7]

        # Level of buildings and related links in village
        fields = {field.get('alt'): field.get('href') for field in fields}

        return fields
