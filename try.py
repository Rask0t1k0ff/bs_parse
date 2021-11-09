from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

driver = webdriver.Chrome(ChromeDriverManager().install())    # here path of driver if it didn't find it.


def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root

driver.get("https://eu.shop.battle.net/en-us/family/world-of-warcraft")
time.sleep(5)
root = driver.find_elements_by_xpath("//div[@id='game']//meka-browsing-card")
print(root)

html_of_interest=driver.execute_script('return arguments[0].innerHTML',root[0])
sel_soup=BeautifulSoup(html_of_interest, 'html.parser')
print(sel_soup )# empty root not expande
print('')
print('')
print('')
print('')
print('')

shadow_root1 = expand_shadow_element(root[0])

html_of_interest=driver.execute_script('return arguments[0].innerHTML',shadow_root1)
sel_soup=BeautifulSoup(html_of_interest, 'html.parser')
print(sel_soup)
