import utils
import re
import tempfile
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
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

    def __init__(self, headless:bool, timeout:int, load_page_attempts:int = 1, homepage:str="https://www.google.com"):
        self.load_page_attempts = load_page_attempts

        self.SELECTORS = utils.load_json("selectors.json")
        # Ensure all required configuration components exist before proceeding
        if not self.SELECTORS:
            raise RuntimeError("Critical error: IMPORTANT DATA NOT LOADED INTO MEMORY. Execution halted.")

        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless=new")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(timeout)

        if self.load_url(homepage):
            print("\033[92mDriver Instance Initialized Successfully!\033[0m")

    def load_url(self, url:str):
        for attempt in range(self.load_page_attempts):
            try:
                self.driver.get(url)
                return True
            except TimeoutException:
                print(f"Timed out waiting for page to load: {url}")
                return False
            except Exception as e:
                print(f"Error loading url (attempt {attempt+1}/{self.load_page_attempts}): {url}.\n{e}")
        return False
    
    def remove_ad(self):
        pass
    def check_results(self) -> bool:
        """Check if there are results and return true else false"""
        return bool(
            self.driver.find_elements(By.CSS_SELECTOR, self.SELECTORS["result_event"])
        )
    def return_results(self) -> list[WebElement]:
        return self.driver.find_elements(By.CSS_SELECTOR, self.SELECTORS["result_event"])
    
    def get_url(self, web_element: WebElement) -> str:
        """Extract a href link from a given WebElement"""
        return web_element.find_element(By.TAG_NAME, "a").get_attribute("href")
    def get_match_info(self) -> WebElement:
        return self.driver.find_element(By.CLASS_NAME, self.SELECTORS["dynamic_selectors"]["match_inf_class"])
    def get_match_scores(self) -> WebElement:
        return self.driver.find_element(By.CLASS_NAME, self.SELECTORS["dynamic_selectors"]["match_result_class"])
    
    def format_match_info(self, text:str):
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        league = lines[0].split(":")[0].strip()
        country = lines[1]
        home_team = lines[2]
        score = lines[3]
        away_team = lines[5]
        
        return {
            "league": league,
            "country": country,
            "home_team": home_team,
            "score": score,
            "away_team": away_team
        }
    def format_match_scores(self, text: str) -> dict:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        headers = lines[0].split()[1:]
        
        match_data = {}
        for index, line in enumerate(lines[1:]):
            parts = line.split()
    
            num_scores = len(headers)
            scores = [int(s) for s in parts[-num_scores:]]
            
            team_name = " ".join(parts[:-num_scores])
            
            team_type = "home" if index == 0 else "away"
    
            quarter_scores = dict(zip(headers[:-1], scores[:-1]))
            
            match_data[team_type] = {
                "name": team_name,
                "quarters": quarter_scores,
                "total": scores[-1]
            }

        return match_data


    # ai generated methods
    def scroll(self, direction: int, knots: int = 5) -> bool:
        """Scrolls the page up or down using simulated mouse wheel clicks (knots).

        :param direction: 0 for DOWN, 1 for UP
        :param knots: The intensity/distance of the scroll (how many wheel
            clicks)
        :return: True if reached the end (bottom when scrolling DOWN, top when
            scrolling UP), False otherwise.

        TESTED AND WORK AS INTENDED
        """
        # Standard mouse wheel click moves ~100 pixels per "knot"
        pixels_per_knot = 100
        scroll_distance = knots * pixels_per_knot

        # Direction 0 = Down (positive delta_y), Direction 1 = Up (negative delta_y)
        if direction == 0:
            delta_y = scroll_distance
        elif direction == 1:
            delta_y = -scroll_distance
        else:
            raise ValueError("Invalid direction: Use 0 for DOWN and 1 for UP.")

        # Execute mouse wheel action
        ActionChains(self.driver).scroll_by_amount(
            delta_x=0, delta_y=delta_y
        ).perform()

        # Check scroll boundary using JavaScript
        if direction == 0:
            # Returns True if at or past the bottom of the page (with a 2px tolerance buffer for high-DPI displays)
            return self.driver.execute_script(
                "return (window.innerHeight + window.scrollY) >= (document.body.scrollHeight - 2);"
            )
        else:
            # Returns True if scrolled all the way to the top
            return self.driver.execute_script("return window.scrollY === 0;")



if __name__ == "__main__":
    engine()