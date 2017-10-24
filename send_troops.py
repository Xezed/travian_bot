from random import randint
from time import sleep

from bs4 import BeautifulSoup

from authorization import logged_in_session


class TroopsOrder:
    """Creates an order for troops and send them to concrete point with timing."""
    def __init__(self, barrack_url=None, troops=None, coords=None, attack_type=None):
        self.barrack_url = barrack_url
        self.session = logged_in_session()
        self.troops = dict(troops)
        self.coords = None
        self.type = dict(attack_type)

    def __call__(self, coords, *args, **kwargs):
        self.coords = dict(coords)
        # self.session = logged_in_session()
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


troops = {'t1': '1',
          't2': '0',
          't3': '0',
          't4': '0',
          't5': '0',
          't6': '0',
          't7': '0',
          't8': '0',
          't9': '0',
          't10': '0',
          't11': '0'}

coords = [
    {'x': '-24', 'y': '-228'},
    {'x': '-23', 'y': '-225'},
    {'x': '-23', 'y': '-224'},
    {'x': '-18', 'y': '-230'},
    {'x': '-25', 'y': '-225'},
    {'x': '-22', 'y': '-223'}
]

attack_type = {'c': 4}
order = TroopsOrder(barrack_url='https://ts7.travian.com/build.php?tt=2&id=39',
                        troops=troops, attack_type=attack_type)

for cord in coords:
    order(cord)
    print('Done!')
    sleep(10+randint(0, 10))
