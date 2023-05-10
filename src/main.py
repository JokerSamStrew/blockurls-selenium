#!/usr/bin/python3

import trio
import json
import argparse
import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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


async def start_listening(listener):
    counter = 0
    async for event in listener:
        counter += 1
        print(counter, 'receive:', event.response.url[:80])


async def event_listener(driver, target):
    async with driver.bidi_connection() as connection:
        session, devtools = connection.session, connection.devtools
        await session.execute(devtools.network.enable())
        counter = 0
        listener = session.listen(devtools.network.ResponseReceived)
        await start_listening(listener)


def get_options():
    options = Options()
    options.add_argument('--incognito')
    options.page_load_strategy = 'eager'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return options


def run():
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=get_options())

    black_list, target = get_args()
    print("black list:", black_list, '\ntarget:', target)

    driver.execute_cdp_cmd(
        'Network.setBlockedURLs', {'urls': black_list})
    driver.execute_cdp_cmd('Network.enable', {})

    p = multiprocessing.Process(
        target=lambda: trio.run(event_listener, driver, target))
    p.start()
    driver.get(target)
    p.join(5)
    if p.is_alive():
        p.kill()
    print(driver.title)
    driver.quit()


if __name__ == "__main__":
    run()
