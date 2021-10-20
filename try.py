import requests
from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def clearing(s):
    s = s.strip()
    s = s.replace("’", "'")
    return s


url = 'https://store.steampowered.com/search/?term='
html_source = requests.get(url).text
soup = Bs(html_source, 'html.parser')
block = soup.find('div', class_='search_results')
name = block.select('span.title')
price = block.select('div.search_price')
for i in range(len(name)):
    print(clearing(name[i].text))
for i in price:
    print(clearing(i.text))