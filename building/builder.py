import re

from abc import ABC, abstractmethod
from asyncio import sleep
from random import randint

from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from check_adventure import check_adventure
from authorization import logged_in_session
from credentials import SERVER_URL
from logger import info_logger_for_future_events


class Builder(ABC):
    """Extendable class for building"""
    def __init__(self, main_page_url):
        self.main_page_url = main_page_url
        self.parser_location_to_build = None
        self.parser_main_page = None
        self.session = None

    async def __call__(self, *args, **kwargs):
        self.session = logged_in_session()
        self.set_parser_of_main_page()
        check_adventure(self.session, self.parser_main_page)
        await self.check_queue()
        self.set_parser_location_to_build()

        successfully_built = await self.build()

        # Trying to build something until success then return True.
        return True if successfully_built else await self.__call__()

    async def build(self):
        """Building function with handle of errors. If success return True, else None"""
        try:
            link_to_build = self.parse_link_to_build()
            self.session.get(link_to_build)

        # Lack of resources raises ValueError. Catch here.
        except ValueError:
            seconds_to_enough = self.parse_seconds_to_enough_resources() + randint(15, 90)

            info_logger_for_future_events('Lack of resources. Will be enough in ', seconds_to_enough)
            await sleep(seconds_to_enough)

        except RequestException:
            info_logger_for_future_events('RequestException occurred. Waiting... Next attempt in', 1500)
            await sleep(1500)

        else:
            self.set_parser_of_main_page()
            seconds_left = await self.parse_seconds_build_left() + randint(15, 90)
            info_logger_for_future_events('Building... Will be completed in ', seconds_left)
            await sleep(seconds_left)

            return True

    async def check_queue(self):
        """If buildings queue is not empty, then sleep until complete."""
        if await self.parse_seconds_build_left():
            seconds_build_left = await self.parse_seconds_build_left()

            info_logger_for_future_events('Something is building already... Will be completed in ', seconds_build_left)
            await sleep(seconds_build_left)

            # Renew the session and parser
            await self.__call__()

    def parse_link_to_build(self):
        """Return a link which starts building if enough resources, else ValueError"""

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
        resource = resource.replace(',', '')

        amount = pattern.search(resource)
        amount = amount.group(0)

        return amount

    def parse_seconds_to_enough_resources(self):
        """Return time in seconds after which will be enough resources to build smth."""

        # TODO handle extend granary/warehouse status
        parsed_class = self.parser_location_to_build.find_all(class_='hide')[0]

        seconds_to_enough_resources = parsed_class.span.get('value')
        seconds_to_enough_resources = int(seconds_to_enough_resources)

        return seconds_to_enough_resources

    async def parse_seconds_build_left(self):
        """Return amount of time in order to build smth."""
        parser = self.parser_main_page
        second_left = parser.find_all(class_='buildDuration')

        # If found buildDuration class then return its value.
        #  Or there is no queue at all so we can build, return 0.
        if second_left:
            second_left = second_left[0].span.get('value')
            second_left = int(second_left)

            if second_left > 0:
                return second_left

            # Event-jam in travian. We can only wait.
            else:
                # 240 seconds to keep session alive.
                info_logger_for_future_events('Event jam. Waiting... Next attempt in ', 240)
                await sleep(240)
                self.set_parser_of_main_page()

                return await self.parse_seconds_build_left()

        return 0

    def is_enough_crop(self):
        """Check if enough crop for building smth new."""
        parse_status_messages = self.parser_location_to_build.find_all(class_='statusMessage')
        if parse_status_messages:
            parse_message = parse_status_messages[0].text

            if parse_message == 'Lack of food: extend cropland first!':
                return False

        return True

    def is_enough_resources(self):
        """Checks amount of resources in order to build something."""
        required_resources = self.parse_required_resources()
        available_resources = self.parse_resources_amount()

        for key in required_resources:
            if (key in available_resources) and (available_resources[key] < required_resources[key]):
                return False

        return True

    def set_parser_of_main_page(self):
        """Renew the parser of the main page"""
        main_page_html = self.session.get(self.main_page_url).text
        self.parser_main_page = BeautifulSoup(main_page_html, 'html.parser')

    @abstractmethod
    def set_parser_location_to_build(self):
        """Set parser to location where will be built new building or field"""
