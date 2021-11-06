from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json


def clearing(s):
    s = s.strip()
    s = s.replace("’", "'")
    return s


browser = webdriver.Chrome(ChromeDriverManager().install())    # here path of driver if it didn't find it.

base = "https://store.steampowered.com/search/?l=english&term="

browser.get(base)

SCROLL_PAUSE_TIME = 0.9

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
href = div.find_all('a', href=True)
imgs = div.find_all('img')
#for i in range(len(name)):
    #print(clearing(name[i].text) + ' - ' + clearing(price[i].text))
product_name = []
price_range = []
product_href = []
product_img = []
for i in name:
    product_name.append(clearing(i.text))
for i in price:
    s = clearing(i.text)
    if s.count('pуб') > 1:
        index = s.find('.')
        price_range.append(s[index + 1:])
    else:
        price_range.append(clearing(i.text))
for i in href:
    product_href.append(i['href'])
for i in imgs:
    product_img.append(i['src'])
with open("steam.json", "w") as write_file:
    data_list = []
    for i in range(len(product_name)):
        data = {'product_name': product_name[i],
                'price_range': price_range[i],
                'product_href': product_href[i],
                'product_img': product_img[i]}
        print(product_name[i] + ' - ' + price_range[i] + ' - ' + product_href[i] + ' - ' + product_img[i])
        data_list.append(data)
    json.dump(data_list, write_file)