import requests
from bs4 import BeautifulSoup as Bs


def clearing(s):
    s = s.strip()
    s = s.replace("’", "'")
    return s


url = 'https://www.epicgames.com/store/ru/browse?sortBy=releaseDate&sortDir=DESC&count=40&start='
count = 0
count_list = []

for i in range(21):
    count_list.append(str(count))
    count += 40

for i in count_list:
    html = requests.get(url+i).text
    soup = Bs(html, 'html.parser')
    ul = soup.find('ul', class_='css-cnqlhg')
    name = ul.select('div.css-1h2ruwl')
    name_2 = []
    for i in range(len(name)):
        if i%2 == 0:
            name_2.append(name[i])
    price = ul.select('span.css-z3vg5b')
    for i in range(len(name_2)):
        print(clearing(name_2[i].text) + ' - ' + clearing(price[i].text))