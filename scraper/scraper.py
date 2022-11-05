from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from time import sleep

MASTER_SERVER = ""
path_to_chrome_profile = "C:\\UNI\\Smarthack\\chrome_profile"


def scrape(json):
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=" + path_to_chrome_profile)
    driver = webdriver.Chrome(options=options)
    driver.get(json["url"])
    driver.implicitly_wait(2)
    raw_elems = driver.find_elements(By.CSS_SELECTOR, json["selecor"][2:])
    elems = []
    for elem in raw_elems:
        elems.append(elem.text)
    return elems


while True:
    response = requests.get(MASTER_SERVER+"api/scraper")
    json = response.json()
    if json["status"] == "empty":
        sleep(10)
        continue

    elems = scrape(json)

    requests.post(MASTER_SERVER+"api/scraper", elems)
    sleep(1)
