from scrapers.base_scraper import BaseScraper
from selenium.webdriver.common.by import By

class ItemScraper(BaseScraper):
    def __init__(self, link=None, output_file=None, wait_time=10, driver=None):
        link = link or "https://www.unwrittenrulebook.com/itemlist.html"
        output_file = output_file or "items.json"
        super().__init__(link=link, output_file=output_file, wait_time=wait_time, driver=driver)

    def scrape(self):
        item_families = ["Med Kits", "Toolboxes", "Maps", "Keys", "Fog Vials", "Flashlight"]
        all_items = []

        items_container = self.wait_for_element_presence(
            By.XPATH, './/section[contains(@class, "container")]//div[contains(@id, "item-container")]'
        )

        items_divs = self.wait_for_all_elements_presence(By.XPATH,
                                                         './/div[contains(@class, "item-type-section")]',
                                                         items_container)

        for div in items_divs:
            item_family = self.get_elements_text(By.XPATH, './/h2[contains(@class, "item-type-header")]', div)

            if item_family not in item_families:
                break

            list_div = div.find_element(By.XPATH, './/div[contains(@class, "survivor-list")]')

            list_sub_divs = self.wait_for_all_elements_presence(By.CSS_SELECTOR,
                                                        "div[class^='survivor-card']",
                                                               list_div)

            addons = []
            items = []

            first = True

            for sub_div in list_sub_divs:
                item_icon = (sub_div.find_element(By.XPATH, './/div[contains(@class, "survivor-image-container")]//img')
                             .get_attribute("src"))

                info_div = self.wait_for_element_presence(By.XPATH,
                                                          ".//div[contains(@class, 'survivor-info')]",
                                                          sub_div)

                if first:
                    addons_btn = self.wait_for_element_to_be_clickable(By.XPATH,
                                                                       ".//div[contains(@class, 'popup-buttons')]"
                                                                       "//button[contains(text(),'View Addons')]", info_div)
                    addons_btn.click()

                    popup_div = self.wait_for_element_presence(By.XPATH,
                                                        ".//div[contains(@id, 'addonsPopup')]"
                                                               "//div[contains(@class, 'popup-content')]")

                    addons_div = popup_div.find_element(By.XPATH, "//div[contains(@id, 'addonsPopupContent')]"
                                                        "//div[contains(@class, 'perk-list')]")
                    addon_divs = addons_div.find_elements(By.CSS_SELECTOR, "div[class^='perk-item']")

                    for addon_div in addon_divs:
                        addon_icon = addon_div.find_element(By.TAG_NAME, "img").get_attribute("src")
                        details_div = addon_div.find_element(By.XPATH, ".//div[contains(@class, 'perk-details')]"
                                                                       "//div[contains(@class, 'perk-name')]")

                        addon_name = self.driver.execute_script("""
                            let element = arguments[0];
                            let childSpans = element.querySelectorAll('span');
                            let text = element.childNodes[0].nodeValue.trim();
                            return text;
                        """, details_div)

                        addon_rarity = details_div.find_element(By.TAG_NAME, "span").text

                        if addon_rarity != "Event":
                            addons.append({"survivor_addon_name": addon_name,
                                           "survivor_addon_rarity": addon_rarity,
                                           "survivor_addon_icon": addon_icon})

                    first = False
                    popup_div.find_element(By.XPATH, ".//button[contains(@class, 'popup-close')]").click()

                item_name = info_div.find_element(By.XPATH, ".//h2").text
                item_rarity = info_div.find_element(By.XPATH, ".//div[contains(@class, 'survivor-badges')]//span").text

                if item_rarity != "Event":
                    items.append({"survivor_item_name": item_name, "survivor_item_rarity": item_rarity, "survivor_item_icon": item_icon})

            item_list = {
                "survivor_item_family": item_family,
                "survivor_items": items,
                "survivor_addons": addons
            }

            all_items.append(item_list)

        return all_items