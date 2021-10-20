import requests
from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def clearing(s):
    s = s.strip()
    s = s.replace("’", "'")
    return s


browser = webdriver.Chrome(ChromeDriverManager().install())    # here path of driver if it didn't find it.

base = "https://store.steampowered.com/search/?term="

browser.get(base)

SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


html_source = browser.page_source
soup = Bs(html_source, 'html.parser')
div = soup.find('div', class_='search_results')
name = div.select('span.title')
price = div.select('div.search_price')
for i in range(len(name)):
    print(clearing(name[i].text) + ' - ' + clearing(price[i].text))