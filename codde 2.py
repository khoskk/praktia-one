import requests
from bs4 import BeautifulSoup  # библиотека для парсинга
import json

# выгрузим гороском для близнецов
url = 'https://1001goroskop.ru/?kn=week'
headers = {
    'User-Agent': 'My User Agent 1.0',  # многие сайты не дают себя парсить ботам
}
response = requests.get(url, headers=headers)


page = response.text
soup = BeautifulSoup(page, "html.parser")

description = soup.find_all('ul', {'class': 'zodi_tbl'})

var = {}

counter = 0
for href in description:
    # print(href)
    links = href.find_all("a")
    for link in links:
        link_url = link["href"]
        title = link["title"]

        full_url = f"https://1001goroskop.ru{link_url}"

        page = requests.get(full_url)

        response = page.text
        soup = BeautifulSoup(response, "html.parser")
        description = soup.find_all('div', {'itemprop': 'description'})

        for elem in description:
            ct = 0
            desc = elem.find_all("p")

            date = elem.find_all("div", {"class": "date"})
            dictionary = {f"{title}":
                            {f"{date[0].text}": f"{desc[0].text}"},
                          }

            for i in range(1, 7):
                dt = date[i].text
                tx = desc[i].text
                dictionary[f"{title}"].update({f"{dt}": f"{tx}"})

            var.update(dictionary)

with open("goroskop.json", "w", encoding="utf-8") as f:
    json.dump(var, f, ensure_ascii=False, indent=4)
