from scrapers.base_scraper import BaseScraper
from selenium.webdriver.common.by import By


class OfferingScraper(BaseScraper):
    def __init__(self, driver=None, link=None, output_file=None, wait_time=10):
        link = link or "https://www.unwrittenrulebook.com/offeringlist.html"
        output_file = output_file or "offerings.json"
        super().__init__(link=link, output_file=output_file, wait_time=wait_time, driver=driver)

    def scrape(self):
        all_offerings = []
        killer_offerings = []
        survivor_offerings = []

        offerings_container = self.wait_for_element_presence(
            By.XPATH, './/section[contains(@class, "container")]//div[contains(@id, "offering-container")]'
        )

        offerings_divs = self.wait_for_all_elements_presence(
            By.XPATH, './/div[contains(@class, "item-type-section")]', offerings_container
        )

        for div in offerings_divs:
            offering_type = div.find_element(By.TAG_NAME, 'h2').text
            list_div = div.find_element(By.XPATH, './/div[contains(@class, "survivor-list")]')
            list_sub_divs = self.wait_for_all_elements_presence(By.CSS_SELECTOR, "div[class^='survivor-card']",
                                                                list_div)

            for subdiv in list_sub_divs:
                offering_icon = (subdiv.find_element(
                    By.XPATH,
                    './/div[contains(@class, "survivor-image-container")]//img').get_attribute("src"))

                info_div = subdiv.find_element(By.XPATH, './/div[contains(@class, "survivor-info")]')
                offering_name = self.get_elements_text(By.XPATH, './/h2[contains(@class, "survivor-name")]', info_div)

                badges = info_div.find_element(By.XPATH, './/div[contains(@class, "survivor-badges")]')
                offering_rarity = self.get_elements_text(By.CSS_SELECTOR, "span[class^='survivor-badge rarity-badge']",
                                                         badges)
                if offering_rarity == "Event":
                    break

                offering_character_type = self.get_elements_text(By.CSS_SELECTOR, "span[class='survivor-badge']",
                                                                 badges)

                offering_data = {"offering_name": offering_name, "offering_rarity": offering_rarity,
                                 "offering_icon": offering_icon, "offering_type": offering_type}

                if offering_character_type == "Killer":
                    killer_offerings.append(offering_data)
                elif offering_character_type == "Survivor":
                    survivor_offerings.append(offering_data)
                elif offering_character_type == "All":
                    all_offerings.append(offering_data)

        return [
            {
                "character_type": "All",
                "offerings": all_offerings,
            },
            {
                "character_type": "Survivor",
                "offerings": survivor_offerings,
            },
            {
                "character_type": "Killer",
                "offerings": killer_offerings,
            },
        ]
