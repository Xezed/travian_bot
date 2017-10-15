import re
import sys

from bs4 import BeautifulSoup

from credentials import SERVER_URL


class BuildField:
    """Build field in village. Type depend on minimum resource"""
    def __init__(self, html, session):
        self.session = session
        self.parser = html

    @property
    def parser(self):
        return self.__dict__['parser']

    @parser.setter
    def parser(self, html):
        # For debugging
        # with open('1.html', 'a') as f:
        #     f.write(html)
        self.__dict__['parser'] = BeautifulSoup(html, 'html.parser')
        
    def build_field(self):
        link_to_field = self.link_field_to_build()
        link_to_build = self.link_to_build(link_to_field)
        self.session.get(link_to_build)
    
    def parse_fields(self):
        # Last link leads to town, so delete its
        fields = self.parser.find_all('area')[:-1]
    
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
        resource = self.parser.find(id=id).text
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
        self.parser = html

        link_to_upgrade = self.parser.find_all(class_='section1')[0].button.get('onclick')

        pattern = re.compile(r'(?<=\').*(?=\')')

        building_link = SERVER_URL + pattern.search(link_to_upgrade).group(0)

        return building_link
