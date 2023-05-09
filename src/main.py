#!/usr/bin/python3
import sys
import os
import trio
import json
import argparse
import time
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.bidi.console import Console
from selenium.webdriver.common.by import By
from selenium.webdriver.common.log import Log
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from functools import partial

TEST_RUN=True

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--black-list')
    parser.add_argument('--target')
    args = parser.parse_args()
    if args.black_list is None:
        print("No blacklist")
        exit(1)
    elif args.target is None:
        print("No target")
        exit(1)

    return json.loads(args.black_list), args.target

async def start_listening(counter, listener):
    async for event in listener:
        counter += 1
        print(counter, 'receive:', event.response.url[:80])

async def test_run(driver, target):
    async with driver.bidi_connection() as connection:
        session, devtools = connection.session, connection.devtools
        await session.execute(devtools.network.enable())
        counter = 0
        listener = session.listen(devtools.network.ResponseReceived)
        async with trio.open_nursery() as nursery:
            nursery.start_soon(partial(start_listening, counter), listener)


def run():
    options = Options()
    options.add_argument('--incognito')
    options.page_load_strategy = 'eager'
    chromedriver_path = os.path.join(os.path.dirname(
        __file__), os.pardir, 'bin', 'chromedriver')

    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
 

    black_list, target = get_args()
    print(black_list, target)

    driver.execute_cdp_cmd(
        'Network.setBlockedURLs', {'urls': black_list})
    driver.execute_cdp_cmd('Network.enable', {})

    if TEST_RUN:
        p = multiprocessing.Process(target=lambda : trio.run(test_run, driver, target))
        print(driver.title)
        p.start()
        driver.get(target)
        p.join(5)
        if p.is_alive():
            p.kill();

    else:
        driver.get(target)
        print(driver.title)

    driver.quit()

if __name__ == "__main__":
    run()
