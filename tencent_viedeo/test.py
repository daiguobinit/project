from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from datetime import timedelta
import time

self_webdrive = webdriver.Chrome()
url = 'https://v.qq.com/'
self_webdrive.get(url)

search = self_webdrive.find_element_by_id('keywords')
search.click()
time.sleep(5)
search.send_keys('勇往直前')

search_btn = self_webdrive.find_element_by_class_name('search_btn')
search_btn.click()

# self_webdrive.switch_to_window('')
a = self_webdrive.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div/h2/a')
a.click()