from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import json

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--verbose')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920, 1200')
chrome_options.add_argument('--disable-dev-shm-usage')


driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.imdb.com/chart/top/")

links = driver.find_elements('xpath', "//a[contains(@class, 'ipc-title-link-wrapper')]")
print(len(links))
sleep(1)

uniq_links = set()
# date = {}
for i in links:
  uniq_links.add(i.get_attribute("href"))

# print(len(uniq_links))  # столько фильмов на одной станице

sleep(1)


movies = driver.find_elements('xpath', "//h3[contains(@class, 'ipc-title__text')]")
uniq_movies = set()
for i in movies:
  if i.text[0].isdigit():
    uniq_movies.add(i.text.split(" ", maxsplit=1)[1])

print(len(uniq_movies))  # столько фильмов на одной станице
# print(uniq_movies)

data = {}
for link in uniq_links:
    driver.get(link)
    try:
        title = driver.find_element('xpath', "//span[contains(@class, 'hero__primary-text')]").text
    except:
        pass
    else:
        if title in uniq_movies:

            # synopsis = driver.find_element('xpath', "//span[contains(@data-testid, 'plot-xs_to_m')]").text
            rating = driver.find_element('xpath', "//span[contains(@class, 'sc-d541859f-1 imUuxf')]").text
            details_block = driver.find_element('xpath', "//div[@data-testid='title-details-section']")
            date = details_block.find_element(By.CLASS_NAME, "ipc-metadata-list-item__list-content-item").text
            date = date.split("(")[0]
            country = driver.find_element('xpath', "//li[@data-testid='title-details-origin']//a").text
            directors_section = driver.find_element('xpath', "//li[@data-testid='title-pc-principal-credit']")
            director = directors_section.find_element(By.CLASS_NAME, "ipc-metadata-list-item__list-content-item").text

            genres_list = []
            genres_section = driver.find_element('xpath', "//div[@data-testid='interests']")
            genres = genres_section.find_elements(By.CLASS_NAME, "ipc-chip__text")
            for genre in genres:
                genres_list.append(genre.text)


            current_movie = {}

            try:
                synopsis = driver.find_element('xpath', "//span[contains(@data-testid, 'plot-xs_to_m')]").text
                current_movie["synopsis"] = synopsis
                try:
                    synopsis = driver.find_element('xpath', "//span[contains(@data-testid, 'plot-l')]").text
                    current_movie["synopsis"] = synopsis
                except:
                    pass
                    try:
                        synopsis = driver.find_element('xpath', "//span[contains(@data-testid, 'plot-xl')]").text
                        current_movie["synopsis"] = synopsis
                    except:
                        pass
            except:
                pass

            # current_movie["synopsis"] = synopsis
            current_movie["rating"] = rating
            current_movie["link"] = link
            current_movie["date"] = date
            current_movie["country"] = country
            current_movie["director"] = director
            current_movie["genres"] = genres_list

            data[title] = current_movie
            # print(title, current_movie)

            # with open("filmData.json", "w", encoding="utf-8") as f:
            #     json.dump(data, f, ensure_ascii=False, indent=4)


    sleep(1)  # нужен таймаут, чтобы драйвер успел перейти на новую страницу

with open("filmData.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print(len(data)) # проверим, что собрали действительно 250 фильмов
