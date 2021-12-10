from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json


def clearing(s):
    s = s.strip()
    s = s.replace("’", "'")
    return s


def expand_shadow_element(element):
    shadow_root = browser.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root


browser = webdriver.Chrome(ChromeDriverManager().install())    # here path of driver if it didn't find it.

base = "https://eu.shop.battle.net/en-us"
base_url = 'https://eu.shop.battle.net'
browser.get(base)
time.sleep(3)
html_source = browser.page_source
soup = Bs(html_source, 'html.parser')
games_block = soup.find('section', class_='app-container')
games_list = games_block.find_all('a', class_='ng-star-inserted')
data_list = []
print(games_list)
name_list = []
for i in range(len(games_list)):
    if i != 1 and i != len(games_list)-1:
        new_url = base_url + games_list[i]['href']
        browser.get(new_url)
        time.sleep(5)
        root = browser.find_elements_by_xpath("//div[@id='game']//meka-browsing-card")
        root2 = browser.find_elements_by_xpath("//div[@id='game']//meka-price-label")
        shadow_root_for_name_img = []
        shadow_root_for_price = []
        html_of_interest = browser.page_source
        sel_soup = Bs(html_of_interest, 'html.parser')
        block = sel_soup.find('div', id='game')
        link_list = block.find_all('a', class_='ng-star-inserted')

        for j in root:
            shadow_root_for_name_img.append(expand_shadow_element(j))

        for j in root2:
            shadow_root_for_price.append(expand_shadow_element(j))

        for j in range(len(shadow_root_for_name_img)):
            html_of_interest = browser.execute_script('return arguments[0].innerHTML', shadow_root_for_name_img[j])
            sel_soup = Bs(html_of_interest, 'html.parser')
            product_name = sel_soup.find('dt', class_='meka-browsing-card__details__name').text
            product_img = sel_soup.find('img')['src']
            html_of_interest = browser.execute_script('return arguments[0].innerHTML', shadow_root_for_price[j])
            sel_soup = Bs(html_of_interest, 'html.parser')
            price_range = sel_soup.find('span', class_='meka-price-label--details__standard-price').text
            product_href = base_url + link_list[j]['href']
            if price_range != 'Learn More' and not (clearing(product_name) in name_list):
                if price_range.find('RUB') != -1:
                    price_range = price_range.replace('RUB', '') + ' руб'
                print(product_name + ' - ' + price_range + ' - ' + product_href + ' - ' + product_img)
                data_dict = {'product_name': clearing(product_name),
                    'price_range': clearing(price_range),
                    'product_href': product_href,
                    'product_img': product_img}
                name_list.append(clearing(product_name))
                data_list.append(data_dict)
with open("battle_net.json", "w") as write_file:
    json.dump(data_list, write_file)

