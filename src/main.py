#!/usr/bin/python3

import os
import trio
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.bidi.console import Console
from selenium.webdriver.common.by import By
from selenium.webdriver.common.log import Log

if __name__ == "__main__":
    options = Options()
    options.add_argument('--incognito')
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options, executable_path=os.path.join(
        os.path.dirname(__file__), os.pardir, 'bin', 'chromedriver'))
    print(driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': [
        '*.css',
        '*.png',
        '*.jpg',
        '*.webp',
        '*.woff2',
        '*gstatic*',
        '*uviewer*',
        '*youtube*'
    ]}))

    driver.get('https://www.google.com')
    search_box = driver.find_element(by=By.NAME, value='q')
    search_box.send_keys('selenium')
    search_box.send_keys(Keys.RETURN)
    driver.execute_cdp_cmd('Network.enable', {})

    input()
    driver.quit()
