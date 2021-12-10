from bs4 import BeautifulSoup as Bs
import requests
import json


def clearing(s):
    s = s.strip()
    s = s.replace("’", "'")
    return s


url = 'https://www.epicgames.com/store/en-US/browse?sortBy=releaseDate&sortDir=DESC&count=40&start='
count = 0
count_list = []

for i in range(22):
    count_list.append(str(count))
    count += 40
data_list = []
with open("epic.json", "w") as write_file:
    for i in count_list:
        html = requests.get(url+i).text
        soup = Bs(html, 'html.parser')
        ul = soup.find('ul', class_='css-cnqlhg')
        name = ul.select('div.css-1h2ruwl')
        name_2 = []
        for j in range(len(name)):
            if j%2 == 0:
                name_2.append(name[j])
        price = ul.select('span.css-z3vg5b')
        href = ul.select('a.css-1jx3eyg')
        #img_blocks = ul.find_all('div', attrs={'data-component': 'Picture'})
        #print(img_blocks)
        for j in range(len(name_2)):
            img = ul.find('img', attrs={'alt': name_2[j].text})
            print(img)
            if price[j].text.find('RUB') != -1:
                pricej = price[j].text.replace('RUB ', '') + ' руб'
            else:
                pricej = price[j].text
            if img['src'][0] == 'd':
                data = {'product_name': name_2[j].text,
                        'price_range': pricej,
                        'product_href': 'https://www.epicgames.com' + href[j]['href'],
                        'product_img': img['data-image'].replace(' ', '%20')}
                print(clearing(name_2[j].text) + ' - ' + clearing(price[j].text) + ' - ' + href[j]['href'] + ' - ' + img['data-image'] + ' ' + i)
            else:
                data = {'product_name': name_2[j].text,
                        'price_range': pricej,
                        'product_href': 'https://www.epicgames.com' + href[j]['href'],
                        'product_img': img['src'].replace(' ', '%20')}
                print(clearing(name_2[j].text) + ' - ' + clearing(price[j].text) + ' - ' + href[j]['href'] + ' - ' + img['src'] + ' ' + i)
            data_list.append(data)
    print(data_list)
    json.dump(data_list, write_file)