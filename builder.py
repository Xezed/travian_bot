import re
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from adventure_check import adventure_check
from authorization import login
from credentials import SERVER_URL


class Builder(ABC):
    """Extendable class for building"""
    def __init__(self, main_page_url):
        self.parser_location_to_build = None
        self.main_page_url = main_page_url
        self.parser_main_page = None
        self.session = None

    def __call__(self, *args, **kwargs):
        """Main function. Gives order to build. Return time which requires to build smth.
            Or raise ValueError if lack of resources."""
        self.session = login()
        self.set_parser_of_main_page()
        adventure_check(self.session, self.parser_main_page)

        # Check queue of buildings.
        if self.parse_time_build_left():
            print('Something is building already.')
            return self.parse_time_build_left()

        link_to_field = self.link_on_location_to_build()
        link_to_build = self.link_to_build(link_to_field)

        # If success return amount of seconds to complete
        try:
            self.session.get(link_to_build)

        except ValueError:
            print('Lack of resources')
            return self.parse_seconds_to_enough_resources()

        else:
            return self.parse_time_build_left()

    @abstractmethod
    def link_on_location_to_build(self):
        """Return link to location where will be built new building or field"""

    def parse_seconds_to_enough_resources(self):
        """Return time in seconds after which will be enough resources to build smth."""

        # TODO handle extend granary/warehouse status
        parsed_class = self.parser_location_to_build.find_all(class_='hide')[0]

        seconds_to_enough_resources = parsed_class.span.get('value')
        seconds_to_enough_resources = int(seconds_to_enough_resources)

        return seconds_to_enough_resources

    def link_to_build(self, link_to_field):
        """Return a link which starts building if enough resources, else ValueError"""

        # open resource field
        html = self.session.get(link_to_field).text
        self.parser_location_to_build = BeautifulSoup(html, 'html.parser')

        # If enough resources parse onclick attribute
        if self.is_enough_resources():
            link_to_upgrade = self.parser_location_to_build.find_all(class_='section1')[0].button.get('onclick')
        else:
            raise ValueError('Lack of resources')

        # parse link to build
        pattern = re.compile(r'(?<=\').*(?=\')')
        building_link = SERVER_URL + pattern.search(link_to_upgrade).group(0)

        return building_link

    def parse_required_resources(self):
        """Return dictionary with resources which required to build smth"""
        required_resources = self.parser_location_to_build.find_all(class_='resources')
        required_resources = {span.get('title').lower(): int(span.contents[1]) for span in required_resources}

        return required_resources

    def parse_resources_amount(self):
        """Return a dict with amount of current resources."""
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
        resource = self.parser_main_page.find(id=id).text
        resource = resource.replace('.', '')

        amount = pattern.search(resource)
        amount = amount.group(0)

        return amount

    def parse_time_build_left(self):
        """Return amount of time in order to build smth."""

        parser = self.parser_main_page
        second_left = parser.find_all(class_='buildDuration')

        # If found buildDuration class then return its value.
        #  Or there is no queue at all so we can build, return 0.
        if second_left:
            second_left = second_left[0].span.get('value')
            second_left = int(second_left)
            return second_left

        return 0

    def is_enough_resources(self):
        """Checks amount of resources in order to build something."""
        required_resources = self.parse_required_resources()
        available_resources = self.parse_resources_amount()
        for key in required_resources.keys():
            if (key in available_resources) and (available_resources[key] < required_resources[key]):
                return False

        return True

    def set_parser_of_main_page(self):
        main_page_html = self.session.get(self.main_page_url).text
        self.parser_main_page = BeautifulSoup(main_page_html, 'html.parser')
