from bs4 import BeautifulSoup

from credentials import SERVER_URL
from logger import get_logger


logger = get_logger(__name__)


def check_adventure(session=None, parser=None):
    """If any of adventures available then go, else do nothing."""
    if is_adventure_available(parser):
        go_to_adventure(session)
        logger.info('Going to adventure')


def go_to_adventure(session):
    hero_page = session.get(SERVER_URL + 'hero.php?t=3').text
    hero_page_parser = BeautifulSoup(hero_page, 'html.parser')
    link_to_adventure = hero_page_parser.find('a', {'class': 'gotoAdventure'})['href']

    confirmation_page = session.get(SERVER_URL + link_to_adventure).text
    confirmation_page_parser = BeautifulSoup(confirmation_page, 'html.parser')
    confirmation_form_inputs = confirmation_page_parser.find_all('input')

    if confirmation_form_inputs:
        data = {tag['name']: tag['value'] for tag in confirmation_form_inputs}
        session.post(SERVER_URL + 'start_adventure.php', data=data)


def is_adventure_available(parser):
    adventure_button = parser.find('button', {'class': 'adventureWhite'})
    adventure_count_tag = adventure_button.find('div', {'class': 'speechBubbleContent'})

    hero_is_available = is_hero_available(parser)

    if adventure_count_tag and hero_is_available:
        return True

    return False


def is_hero_available(parser):
    hero_is_not_available = parser.find('img', {'alt': 'on the way'})
    hero_is_available = not bool(hero_is_not_available)

    return hero_is_available
