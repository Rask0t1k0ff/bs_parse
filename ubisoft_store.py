import requests
from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json


def clearing(s):
    s = s.strip()
    s = s.replace("’", "'")
    s = s.replace('Одиссея', 'Odyssey')
    s = s.replace('Вальгалла', 'Valhalla')
    s = s.replace('ВАЛЬГАЛЛА', 'Valhalla')
    return s


def scrolling(base):

    browser.get(base)

    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-1200);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html_source = browser.page_source
    return Bs(html_source, 'html.parser')


browser = webdriver.Chrome(ChromeDriverManager().install())    # here path of driver if it didn't find it.


soup = scrolling('https://store.ubi.com/ru/games')
div = soup.find('div', class_='search-result-content')
li = div.find_all('li', attrs={'class': ['grid-tile', 'cell', 'shrink', 'grid-tile--auto']})
data_list = []
for i in range(len(li)):
    name = li[i].select('div.prod-title')
    img = li[i].find('img', attrs={'class': ['product_image', 'primary-image', 'card-image']})
    link = li[i].find('a', class_='thumb-link')
    edition = li[i].find('div', class_='card-subtitle')
    price = li[i].find_all('span', attrs={'class': ['price-sales', 'standard-price']})
    free_or_soon = li[i].find('div', class_='product-availability-label')
    if price != []:
        data_dict = {'product_name': clearing(name[0].text) + ' ' + clearing(edition.text),
                    'price_range': clearing(price[0].text).replace('₽', 'руб'),
                    'product_href': 'https://store.ubi.com' + link['href'],
                    'product_img': img['data-src']}
        print(clearing(name[0].text) + ' ' + clearing(edition.text) + ' - ' + link['href'])
        data_list.append(data_dict)
with open("ubisoft.json", "w") as write_file:
    json.dump(data_list, write_file)



