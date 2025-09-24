import os
from dotenv import load_dotenv

from scrapers.modules.survivor_scraper import SurvivorScraper
from scrapers.modules.killer_scraper import KillerScraper
from scrapers.modules.offering_scraper import OfferingScraper
from scrapers.modules.perk_scraper import PerkScraper
from scrapers.modules.item_scraper import ItemScraper

load_dotenv()
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

def run_scrapers():
    scrapers = [
        # SurvivorScraper(),
        # KillerScraper(),
        # PerkScraper(),
        # ItemScraper(),
        OfferingScraper(),
    ]

    for scraper in scrapers:
        scraper.run()


if __name__ == "__main__":
    run_scrapers()