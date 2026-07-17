import utils
import re
import tempfile
from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from webdriver_manager.chrome import ChromeDriverManager #this library automatically downloads the latest version of chrome webdriver so that i do not have to manually download a new version everything that chrome get an update


class engine:

    # hints
    driver: WebDriver


    def __init__(self):
        SETTINGS = utils.load_json("settings.json")
        SELECTORS = utils.load_json("selectors.json")
        URLS = utils.load_json("urls.json")

        # Ensure all required configuration components exist before proceeding
        # if not all([SETTINGS, SELECTORS, URLS]):
        #     raise RuntimeError("Critical error: IMPORTANT DATA NOT LOADED INTO MEMORY. Execution halted.")

        chrome_options = Options()

        if SETTINGS["Defaults"]["Headless"]:
            chrome_options.add_argument("--headless=new")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        self.driver.implicitly_wait(SETTINGS["Defaults"]["Timeout"])
        print(f"Attempts: {SETTINGS['Defaults']['Load_Page_Attempts']}")

        if self.load_url(SETTINGS["Homepage"], SETTINGS["Defaults"]["Load_Page_Attempts"]):
            print("\033[92mDriver Instance Initialized Successfully!\033[0m")
        
        # input("Press Enter to close the browser...")

    def load_url(self, url:str, attempts = 0):
        print(f"Loading url")
        for attempt in range(attempts):
            try:
                self.driver.get(url)
                return True
                
            except TimeoutException:
                print(f"Timed out waiting for page to load: {url}")
                return False
            except Exception as e:
                print(f"Error loading url (attempt {attempt+1}/{attempts}): {url}.\n{e}")
        
        return False
    def remove_ad(self):
        pass


if __name__ == "__main__":
    engine()