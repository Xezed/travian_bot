from random import randint
from asyncio import sleep
from datetime import datetime

from bs4 import BeautifulSoup

from authorization import logged_in_session

ATTACK_TYPE = {'c': 4}

TROOPS = {'t' + str(i): 0 for i in range(1, 12)}


class TroopsOrder:
    """Creates an order for troops and send them to concrete point with timing."""

    def __init__(self, barrack_url=None, coords=None):
        self.barrack_url = barrack_url
        self.coords = dict(coords)
        self.session = None
        self.time_to_come_back = None
        self.troops = None
        self.type = dict(ATTACK_TYPE)

    def __call__(self, *args, **kwargs):
        self.session = logged_in_session()
        self.parse_troops_amount()

        # If none of troops are available then wait.
        if not self.what_troops_available():
            sleep(3600)
            self.__call__()

        self.send_troops()

    def send_troops(self):
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
        self.parse_time_to_come_back(confirmation_parser)

        hidden_inputs_tags = confirmation_parser.find_all('input', {'type': 'hidden'})
        post_data = {tag['name']: tag['value'] for tag in hidden_inputs_tags}

        post_data['s1'] = 'ok'

        self.session.post(self.barrack_url, data=post_data)

    def parse_troops_amount(self):
        overview_page_link = self.barrack_url.replace('?tt=2', '?tt=1')
        overview_page = self.session.get(overview_page_link).text
        overview_page_parser = BeautifulSoup(overview_page, 'html.parser')

        # Get tags with amount of units.
        unit_amount_tags = overview_page_parser.find_all('td', class_='unit')
        unit_name_tags = overview_page_parser.find_all('img', class_='unit')

        # Create dictionary with troops information
        troops_amount = {name['alt']: amount.text for name, amount in zip(unit_name_tags, unit_amount_tags)}
        self.troops = troops_amount

    def parse_time_to_come_back(self, confirmation_parser):
        """Compute time to raid and come back to village. Takes parser of confirmation page"""
        timer_element = confirmation_parser.find('div', class_='at').contents[1]

        arrival_time_in_seconds = int(timer_element['value'])

        arrival_time = datetime.fromtimestamp(arrival_time_in_seconds) - datetime.now()

        seconds_to_arrive = arrival_time.total_seconds()
        time_to_come_back = seconds_to_arrive * 2

        self.time_to_come_back = time_to_come_back

    def what_troops_available(self):
        """Determine what type of troops will be sent based on their availability. Return type and amount"""
        if int(self.troops['Theutates Thunder']) >= 20:
            return {'t4': "20"}

        if int(self.troops['Phalanx']) >= 10:
            return {'t1': "10"}


# TroopsOrder(barrack_url='https://ts7.travian.com/build.php?tt=2&id=39', coords={'x': '-24', 'y': '-228'})()