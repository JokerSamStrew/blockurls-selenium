#!/usr/bin/python3
# Description: The Python code below will search selenium in Google.

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
 
options = Options()
options.binary_location = os.path.join(os.path.dirname(__file__), os.pardir, 'bin')
driver = webdriver.Chrome(executable_path=os.path.join(os.path.dirname(__file__), os.pardir, 'bin', 'chromedriver.exe'))

driver.get("https://www.google.com")
search_box = driver.find_element(by=By.NAME, value='q')  # Find search input box.
search_box.send_keys('selenium')               # Type in selenium.
search_box.send_keys(Keys.RETURN)              # Press ENTER.

input()
# Close.
#driver.close()