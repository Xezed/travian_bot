import requests

from authorization import login
from parse_village_fields import build_field


def main():
    with requests.session() as session:
        html = login(session)
        build_field(html, session)


if __name__ == '__main__':
    main()
