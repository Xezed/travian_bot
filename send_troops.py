import os

from asyncio import sleep
from datetime import datetime
from time import time

from bs4 import BeautifulSoup

from authorization import logged_in_session
from logger import info_logger_for_future_events

ATTACK_TYPE = {'c': 4}

TROOPS = {'t' + str(i): 0 for i in range(1, 12)}


class TroopsOrder:
    """Creates an order for troops and send them to concrete point with timing."""

    def __init__(self, barrack_url=None, coords=None, time_of_next_raid=0):
        self.barrack_url = barrack_url
        self.coords = dict(coords)
        self.session = None
        self.time_of_next_raid = float(time_of_next_raid)
        self.troops = None
        self.type = dict(ATTACK_TYPE)

    async def __call__(self, *args, **kwargs):
        self.session = logged_in_session()

        time_to_next_raid = self.time_of_next_raid - time()

        if time_to_next_raid > 0:
            info_logger_for_future_events('Raid was recently. Next raid in: ', time_to_next_raid)
            await sleep(time_to_next_raid)
            await self.__call__()

        self.parse_troops_amount()

        # If none of troops are available then wait.
        if not self.what_troops_available():
            info_logger_for_future_events('Troops are not available. Waiting till... ', 3600)
            await sleep(3600)
            await self.__call__()

        self.send_troops()
        self.save_next_raid_time()
        time_to_next_raid = self.time_of_next_raid - time()

        info_logger_for_future_events('Raiding... Next raid in: ', time_to_next_raid)
        await sleep(time_to_next_raid)
        await self.__call__()

    def send_troops(self):
        """The main function"""
        barrack_page = self.session.get(self.barrack_url).text
        barrack_parser = BeautifulSoup(barrack_page, 'html.parser')

        hidden_inputs_tags = barrack_parser.find_all('input', {'type': 'hidden'})

        post_data = {tag['name']: tag['value'] for tag in hidden_inputs_tags}

        post_data.update(TROOPS)
        post_data.update(self.what_troops_available())
        post_data.update(self.coords)
        post_data.update(self.type)
        post_data['dname'] = ''
        post_data['s1'] = 'ok'

        confirmation = self.session.post(self.barrack_url, data=post_data).text

        confirmation_parser = BeautifulSoup(confirmation, 'html.parser')
        self.parse_time_of_next_raid(confirmation_parser)

        hidden_inputs_tags = confirmation_parser.find_all('input', {'type': 'hidden'})
        post_data = {tag['name']: tag['value'] for tag in hidden_inputs_tags}
        post_data['s1'] = 'ok'

        self.session.post(self.barrack_url, data=post_data)

    def parse_troops_amount(self):
        """Parse amount of troops and save of to property"""
        overview_page_link = self.barrack_url.replace('tt=2', 'tt=1')
        overview_page = self.session.get(overview_page_link).text
        overview_page_parser = BeautifulSoup(overview_page, 'html.parser')

        # Get tags with amount of units.
        unit_name_tags = overview_page_parser.find_all('img', class_='unit')
        unit_amount_tags = overview_page_parser.find_all('td', class_='unit')

        # Create dictionary with troops information
        troops_amount = {name['alt']: amount.text for name, amount in zip(unit_name_tags, unit_amount_tags)}
        self.troops = troops_amount

    def parse_time_of_next_raid(self, confirmation_parser):
        """Compute time to next raid. Takes parser of confirmation page"""
        timer_element = confirmation_parser.find('div', class_='at').contents[1]

        arrival_time_in_seconds = int(timer_element['value'])
        arrival_time = datetime.fromtimestamp(arrival_time_in_seconds) - datetime.now()

        seconds_to_come_back = arrival_time.total_seconds() * 2
        come_back_time = time() + seconds_to_come_back

        self.time_of_next_raid = come_back_time

    def save_next_raid_time(self):
        """Save coords and time for next raid in file."""
        with open("raids.txt", "rt") as file_input:
            with open("new_raids.txt", "wt") as file_output:

                for line in file_input:
                    if str(self.coords) in line:
                        file_output.write(str(self.coords) + ';' + str(self.time_of_next_raid) + '\n')
                    else:
                        file_output.write(line)

        os.rename('new_raids.txt', "raids.txt")

    def what_troops_available(self):
        """Determine what type of troops will be sent based on their availability. Return type and amount"""
        if int(self.troops['Theutates Thunder']) >= 20:
            return {'t4': '20'}
