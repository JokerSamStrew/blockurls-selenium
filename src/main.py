#!/usr/bin/python3

import os
import trio
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.bidi.console import Console
from selenium.webdriver.common.by import By
from selenium.webdriver.common.log import Log
from functools import partial

BLACK_LIST = [
    '*.css',
    '*.png',
    '*.ico',
    '*.jpg',
    '*.webp',
    '*.woff2',
    '*gstatic*',
    '*uviewer*',
    '*youtube*',
    'data:image*'
]


def test_code(driver):
    driver.get('https://www.google.com')
    search_box = driver.find_element(by=By.NAME, value='q')
    search_box.send_keys('selenium')
    search_box.send_keys(Keys.RETURN)


async def start_listening(counter, listener):
    async for event in listener:
        counter += 1
        print(counter, event.response.url[:80])


async def run():
    options = Options()
    options.add_argument('--incognito')
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options, executable_path=os.path.join(
        os.path.dirname(__file__), os.pardir, 'bin', 'chromedriver'))

    print(driver.execute_cdp_cmd(
        'Network.setBlockedURLs', {'urls': BLACK_LIST}))
    driver.execute_cdp_cmd('Network.enable', {})

    async with driver.bidi_connection() as connection:
        session, devtools = connection.session, connection.devtools
        await session.execute(devtools.network.enable())
        counter = 0
        listener = session.listen(devtools.network.ResponseReceived)
        async with trio.open_nursery() as nursery:
            # start_listening blocks, so we run it in another coroutine
            nursery.start_soon(partial(start_listening, counter), listener)
            test_code(driver)

if __name__ == "__main__":
    trio.run(run)
    input()
    driver.quit()
