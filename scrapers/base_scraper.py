import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

class BaseScraper:
    def __init__(self, link: str, output_file: str, wait_time: int = 10, driver: webdriver.Chrome = None):
        self.link = link
        self.output_file = output_file
        self.wait_time = wait_time

        if driver is None:
            service = Service(CHROMEDRIVER_PATH)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            self.driver = driver

    def get_driver(self):
        return self.driver

    def wait_for_element_presence(self, by, locator, root=None):
        root = root or self.driver

        return WebDriverWait(root, self.wait_time).until(
            EC.presence_of_element_located((by, locator))
        )

    def wait_for_all_elements_presence(self, by, locator, root=None):
        root = root or self.driver

        return WebDriverWait(root, self.wait_time).until(
            EC.presence_of_all_elements_located((by, locator))
        )

    def get_elements_text(self, by, locator, root=None):
        root = root or self.driver

        return WebDriverWait(root, 20).until(
            EC.visibility_of_element_located((by, locator))
        ).text

    def wait_for_element_to_be_clickable(self, by, locator, root=None):
        root = root or self.driver

        return WebDriverWait(root, self.wait_time).until(
            EC.element_to_be_clickable((by, locator))
        )

    def scrape(self):
        raise NotImplementedError

    def save_json(self, data):
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        DATA_DIR = os.path.join(BASE_DIR, "data")
        os.makedirs(DATA_DIR, exist_ok=True)

        file_path = os.path.join(DATA_DIR, self.output_file)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def run(self):
        print(f"Starting scraper for {self.link}")

        try:
            self.driver.get(self.link)
            data = self.scrape()
            self.save_json(data)
            print(f"Successfully scraped from {self.link}\n")

        except Exception as e:
            print(f"Error scraping {self.link}: {e}")
        finally:
            self.driver.quit()