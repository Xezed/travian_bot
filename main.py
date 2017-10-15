import requests

from authorization import login
from parse_village_fields import BuildField


def main():
    with requests.session() as session:
        html = login(session)
        build_field = BuildField(html, session)
        build_field.build_field()
        print('success!')


if __name__ == '__main__':
    main()
