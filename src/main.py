#!/usr/bin/python3
# Description: The Python code below will search selenium in Google.

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

 
options = Options()
options.add_argument("--incognito")
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options, executable_path=os.path.join(os.path.dirname(__file__), os.pardir, 'bin', 'chromedriver'))
print(driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": [
    "*.css",
    "*.png",
    "*.jpg", 
    "*.webp",
    "*.woff2",
    "*gstatic*",
    "*uviewer*",
    "*youtube*"
    ]}))

print(driver.execute_cdp_cmd('Network.enable', {}))

driver.get("https://www.google.com")
search_box = driver.find_element(by=By.NAME, value='q')  # Find search input box.
search_box.send_keys('selenium')               # Type in selenium.
search_box.send_keys(Keys.RETURN)              # Press ENTER.

input()
# Close.
#driver.close()