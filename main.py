import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

# Website URL
homepage_url = "https://www.masterduelmeta.com"
topdecks_url = "https://www.masterduelmeta.com/top-decks#page="
topdecks_full_url = "https://www.masterduelmeta.com/top-decks#dateRange=All%20time&page="

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/117.0.0.0 Safari/537.36"
}

# Browser Settings
options = Options()
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
options.add_argument('--disable-extensions')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.page_load_strategy='none'

service = Service()
driver = webdriver.Chrome(service=service, options=options)
browser = webdriver.Chrome()
browser_deck = webdriver.Chrome()

# Page range of the scraped web pages
start_page = 1
end_page = 3001

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    response = requests.get(topdecks_url, headers=headers)

    # If the webpage response is normal
    if response.ok:
        print("response OK!")

        browser.get(topdecks_url)
        time.sleep(10)
        page_url = topdecks_full_url
        browser.refresh()
        browser.get(page_url + f"{1}")

        # Loop through each page of the deck table
        for page_num in range(start_page, end_page):
            time.sleep(1)
            topdecks_page = browser.page_source
            soup = BeautifulSoup(topdecks_page, "html.parser")

            # Locate the position of the table in the HTML
            allRows = soup.findAll("td", attrs={"class": "deck-img-container svelte-h85nr5"})

            # Loop through each row in the table
            for row in allRows:
                # Get the URLs of each deck page
                deckpage_header = row.findAll("a")
                deckpage_url = deckpage_header[0].attrs["href"]
                full_url = homepage_url + deckpage_url
                response_deck = requests.get(full_url, headers=headers)
                # If the webpage response is normal
                if response_deck.ok:
                    try:
                        print("response_deck OK!")
                        # Redirect to the deck page
                        browser_deck.get(full_url)
                        locaterShareButton = (By.CLASS_NAME, 'svelte-14r22mt')
                        # Click the "Share" button
                        browser_deck.refresh()
                        clickShareButton = WebDriverWait(browser_deck, 20).until(
                            EC.element_to_be_clickable(locaterShareButton))
                        time.sleep(1)
                        clickShareButton.click()
                        print("Share Button Clicked!")
                        # Click the "as YDK File" button
                        locaterSaveButtons = (By.CLASS_NAME, "listItem")
                        clickSaveButtons = WebDriverWait(browser_deck, 20).until(
                            EC.presence_of_all_elements_located(locaterSaveButtons))
                        time.sleep(1)
                        clickSaveButtons[3].click()
                        print("Save Button Clicked!")
                    except Exception as e:
                        pass
                else:
                    print(response_deck.status_code)
                time.sleep(1)
            browser.execute_script('document.getElementsByClassName("jump-container svelte-10rnaaj")[1].getElementsByClassName("svelte-10rnaaj")[0].click();')

    else:
        print(response.status_code)
