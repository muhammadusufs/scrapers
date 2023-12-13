import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.olx.uz/nedvizhimost/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

get_pagination_number = int(soup.select('li[data-testid="pagination-list-item"]')[-1].text)

data = []



for p in range(1, get_pagination_number + 1):
    pagination_url = f"https://www.olx.uz/nedvizhimost/?page={p}"
    print(pagination_url)
    response = requests.get(pagination_url)
    page_content = BeautifulSoup(response.content, "html.parser")

    results = page_content.find("div", {"class":"css-oukcj3"}).findAll("div", {"class":"css-1sw7q4x"})

    for r in results:
        card = r.find("a", {"class":"css-rc5s2u"}).find("div", {"class":"css-qfzx1y"}).find("div", {"class":"css-1venxj6"})
        title = card.find("div", {"class":"css-1apmciz"}).find("div", {"class":"css-u2ayx9"}).find("h6").text
        price = card.find("div", {"class":"css-1apmciz"}).find("div", {"class":"css-u2ayx9"}).find("p").text

        address = card.find("div", {"class":"css-1apmciz"}).find("div", {"class":"css-odp1qd"}).find("p").text.split("-")[0].strip()
        capacity =  card.find("div", {"class":"css-1apmciz"}).find("div", {"class":"css-odp1qd"}).find("div", {"class":"css-1kfqt7f"}).find("span")

        capacity_text = capacity.text if capacity else None

        ad = {
            'title':title,
            'price':price,
            'address':address,
            'capacity':capacity_text
        }
        
        data.append(ad)

file = 'data.json'

with open(file, 'w', encoding='utf8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"\nOlingan jami ma'lumotlar soni : {len(data)}")
print("Ma'lumotlar data.json faylida saqlandi\n\n")
