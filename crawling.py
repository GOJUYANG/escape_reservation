import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


WEB_DRIVER_PATH = "./chromedriver.exe"

s = Service(WEB_DRIVER_PATH)
driver = webdriver.Chrome(service=s)
driver.get("http://newescape.co.kr/room/")

html = driver.find_element(By.TAG_NAME, 'html')

theme_menu = driver.find_element(By.CLASS_NAME, 'tab_menu')
theme_tab = theme_menu.find_element(By.CSS_SELECTOR, '#contents > div > div.tab_menu > ul')

theme_name_list = []

theme_names = WebDriverWait(theme_tab, timeout=9999).until(
    lambda t: t.find_elements(By.TAG_NAME, 'li'))
for theme in theme_names:
    if theme.text == '':
        pass
    else:
        theme_name_list.append(theme.text)

for i, theme in enumerate(theme_names):
    time.sleep(1)
    theme.click()


print(theme_name_list)

while True:
    pass