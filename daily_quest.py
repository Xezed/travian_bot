"""Stand-alone one-off file for quest."""

from random import randint
from time import sleep

from bs4 import BeautifulSoup

from authorization import logged_in_session


ATTACK_TYPE = {'c': 4}

coords = [
    {'x': '-24', 'y': '-228'},
    {'x': '-23', 'y': '-225'},
    {'x': '-23', 'y': '-224'},
]

TROOPS = {'t' + str(i): 0 for i in range(1, 12)}
TROOPS['t1'] = 1


class TroopsOrder:
    def __init__(self, barrack_url=None, troops=None, attack_type=None):
        self.barrack_url = barrack_url
        self.session = logged_in_session()
        self.troops = dict(troops)
        self.coords = None
        self.type = dict(attack_type)

    def __call__(self, coords, *args, **kwargs):
        self.coords = dict(coords)
        self.send_troops()

    def send_troops(self):
        barrack_page = self.session.get(self.barrack_url).text
        barrack_parser = BeautifulSoup(barrack_page, 'html.parser')

        hidden_inputs_tags = barrack_parser.find_all('input', {'type': 'hidden'})

        post_data = {tag['name']: tag['value'] for tag in hidden_inputs_tags}
        post_data.update(self.troops)
        post_data.update(self.coords)
        post_data.update(self.type)
        post_data['dname'] = ''
        post_data['s1'] = 'ok'

        confirmation = self.session.post(self.barrack_url, data=post_data).text

        confirmation_parser = BeautifulSoup(confirmation, 'html.parser')

        hidden_inputs_tags = confirmation_parser.find_all('input', {'type': 'hidden'})
        post_data = {tag['name']: tag['value'] for tag in hidden_inputs_tags}

        post_data['s1'] = 'ok'

        self.session.post(self.barrack_url, data=post_data)


order = TroopsOrder(barrack_url='https://ts7.travian.com/build.php?tt=2&id=39',
                    troops=TROOPS, attack_type=ATTACK_TYPE)

for cord in coords:
    order(cord)
    print('Done!')
    sleep(10+randint(0, 10))
