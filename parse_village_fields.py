import re
import sys

from bs4 import BeautifulSoup

from credentials import SERVER_URL


class BuildField:
    """Build field in village. Type depend on minimum resource"""
    def __init__(self, html, session):
        self.session = session
        self.parser_field_to_build = None
        self.parser_village_page = BeautifulSoup(html, 'html.parser')

    def build_field(self):
        # Check queue of buildings.
        if self.parse_time_build_left():
            print('Something is building already.')
            return self.parse_time_build_left()

        link_to_field = self.link_field_to_build()
        link_to_build = self.link_to_build(link_to_field)

        # If success return amount of seconds to complete
        try:
            self.session.get(link_to_build)
        except ValueError:
            print('Lack of resources')
        else:
            return self.parse_time_build_left()
    
    def parse_fields(self):
        # Last link leads to town, so delete its
        fields = self.parser_village_page.find_all('area')[:-1]
    
        # Level of buildings and related links in village
        fields = {field.get('alt'): field.get('href') for field in fields}

        return fields
    
    def parse_resources_amount(self):
        lumber = int(self.parse_resource('l1'))
        clay = int(self.parse_resource('l2'))
        iron = int(self.parse_resource('l3'))
        crop = int(self.parse_resource('l4'))

        resources_amount = {'lumber': lumber, 'clay': clay,
                            'iron': iron, 'crop': crop}
        return resources_amount
    
    def parse_resource(self, id):
        """Takes id of resource-tag in html and return amount of this resource"""
        pattern = re.compile(r'\d+')
        resource = self.parser_village_page.find(id=id).text
        resource = resource.replace('.', '')

        amount = pattern.search(resource)
        amount = amount.group(0)

        return amount

    def link_field_to_build(self):
        """Select field where will be built new resource-field"""

        # Find minimal resource and parse fields
        resources_amount = self.parse_resources_amount()
        minimal_resource = min(resources_amount, key=resources_amount.get)
        fields = self.parse_fields()

        lowest_level = sys.maxsize
        field_link = None
    
        # wood name in html for lumber, so need to change
        if minimal_resource == 'lumber':
            minimal_resource = 'wood'
    
        for field, link in fields.items():
            fields_level = int(field[-1])
            if (minimal_resource in field.lower()) and (fields_level < lowest_level):
                lowest_level = fields_level
                field_link = link

        return SERVER_URL + field_link

    def link_to_build(self, building_link):
        """Return a link which start building"""
        html = self.session.get(building_link).text
        self.parser_field_to_build = BeautifulSoup(html, 'html.parser')

        if self.is_enough_resources():
            link_to_upgrade = self.parser_field_to_build.find_all(class_='section1')[0].button.get('onclick')
        else:
            raise ValueError('Lack of resources')

        pattern = re.compile(r'(?<=\').*(?=\')')

        building_link = SERVER_URL + pattern.search(link_to_upgrade).group(0)

        return building_link

    def is_enough_resources(self):
        required_resources = self.parse_required_resources()
        available_resources = self.parse_resources_amount()
        for key in required_resources.keys():
            if (key in available_resources) and (available_resources[key] < required_resources[key]):
                return False

        return True

    def parse_required_resources(self):
        required_resources = self.parser_field_to_build.find_all(class_='resources')
        required_resources = {span.get('title').lower(): int(span.contents[1]) for span in required_resources}

        return required_resources

    def parse_time_build_left(self):
        parser = self.parser_village_page
        second_left = parser.find_all(class_='buildDuration')[0].span.get('value')
        if second_left:
            second_left = int(second_left)

        return second_left


