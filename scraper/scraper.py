from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from time import sleep

MASTER_SERVER = "http://localhost:8069/"
path_to_chrome_profile = r"C:\Users\lmg\Desktop\NoCodeWebScraper\scraper\chrome_profile"


class Scraper:
    def get_scrape_entries(url, selector):
        options = webdriver.ChromeOptions()
        options.add_argument(r"--user-data-dir=" + path_to_chrome_profile)
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.implicitly_wait(2)
        raw_elems = driver.find_elements(By.CSS_SELECTOR, selector[2:])
        elems = []
        for elem in raw_elems:
            elems.append(elem.text)
        return elems


class ScrapeBatchProcessor:
    scraper_ = Scraper()

    def realtime_batch_loop():
        while True:
            response = requests.get(MASTER_SERVER+"api/scraper")
            expired_scrapes = response.json()
            if expired_scrapes["status"] == "empty":
                print("No job ;{")
                sleep(10)
                continue

            new_scrapes = []
            for scrape in expired_scrapes["job"]["scrapes"]:
                entries = Scraper.get_scrape_entries(expired_scrapes["job"]["url"],
                                                     scrape["selector"])
                new_scrapes.append(entries)

            requests.post(
                MASTER_SERVER+"api/scraper",
                json={
                    "status": "OK",
                    "id": expired_scrapes["job"]["id"],
                    "scrapes": new_scrapes
                })
            sleep(1)


if __name__ == "__main__":
    ScrapeBatchProcessor.realtime_batch_loop()
