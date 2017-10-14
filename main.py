import asyncio
import os

import aiohttp
import async_timeout
from bs4 import BeautifulSoup


LOGIN_URL = 'https://ts7.travian.com/dorf1.php'
LOGIN_USERNAME = os.environ['LOGIN_USERNAME']
LOGIN_PASSWORD = os.environ['LOGIN_PASSWORD']


# async def fetch(session, url):
#     with async_timeout.timeout(10):
#         async with session.get(url) as response:
#             return await response.text()


async def login(session, url):
    data = {
        'name': LOGIN_USERNAME,
        'password': LOGIN_PASSWORD,
        's1': 'Login',
        'w': '1366:768',
        'login': login
    }

    async with session.post(url, data=data) as resp:
        return await resp.text()


async def build(session, url):
    params = {'a': '14', 'c': '631a60'}

    async with session.get(url, params=params) as resp:
        return await resp.text()


async def main():
    async with aiohttp.ClientSession() as session:
        html = await login(session, LOGIN_URL)
        parser = BeautifulSoup(html, 'html.parser')
        areas = parser.find_all('area')
        print(areas)
        # html = await build(session, LOGIN_URL)
        # with open('login.html', 'w', encoding='utf-8') as f:
        #     f.write(html)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())