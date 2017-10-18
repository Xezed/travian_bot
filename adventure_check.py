from bs4 import BeautifulSoup

from credentials import SERVER_URL


def adventure_check(session=None, parser=None):
    if is_adventure_available(parser):
        go_to_adventure(session)


def go_to_adventure(session):
    hero_page = session.get('https://ts7.travian.com/hero.php?t=3').text
    hero_page_parser = BeautifulSoup(hero_page, 'html.parser')
    link_to_adventure = hero_page_parser.find('a', {'class': 'gotoAdventure'})['href']

    print(SERVER_URL + link_to_adventure)

    confirmation_page = session.get(SERVER_URL + link_to_adventure).text
    confirmation_page_parser = BeautifulSoup(confirmation_page, 'html.parser')
    confirmation_form_inputs = confirmation_page_parser.find_all('input')

    if confirmation_form_inputs:
        data = {tag['name']: tag['value'] for tag in confirmation_form_inputs}
        session.post(SERVER_URL + 'start_adventure.php', data=data)


def is_adventure_available(parser):
    adventure_button = parser.find('button', {'class': 'adventureWhite'})
    adventure_count_tag = adventure_button.find('div', {'class': 'speechBubbleContent'})
    print(adventure_count_tag)
    if adventure_count_tag:
        return True

    return False
