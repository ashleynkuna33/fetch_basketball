from engine import engine
from files import FileHandler
import utils

from multiprocessing import Pool
import time

class Basketball:
    def __init__(self):

        URLS = utils.load_json("urls.json")
        SETTINGS = utils.load_json("settings.json")
        if not all([URLS, SETTINGS]):
            raise RuntimeError("Critical error: IMPORTANT DATA NOT LOADED INTO MEMORY. Execution halted.")
        
        self.data = FileHandler(SETTINGS["Path"],SETTINGS["Defaults"]["create_keys"],SETTINGS['Defaults']["data_encoding"])

        if SETTINGS["Actions"]["Scrape_league"]:
            print("League Job Started")

            league_chunks = []

            with Pool(processes=SETTINGS["Defaults"]["Threads"]) as pool:
                pool.starmap(Basketball.leagues, [(i, urls, self.data, SETTINGS) for i, urls in enumerate(league_chunks)])

            for name, url in URLS["Leagues"].items():
                print(f"\nName: {name}\nUrl: {url}\n")

        
        if SETTINGS["Actions"]["Scrape_team"]:
            print("League Job Started")
    
    # def chuck_list(self, URLS, SETTINGS, type):

    #     threads = SETTINGS["Defaults"]["Threads"]

    #     chunks = [[] for _ in range(threads)]
    #     stride = self.threads * step

    #     for thread_index in range(self.threads):
    #         index = thread_index * step
    #         while index < len(data):
    #             chunks[thread_index].extend(data[index:index + step])
    #             index += stride

    #     return chunks

    @staticmethod
    def leagues(thread_num,urls,data, SETTINGS):
        """
        Process of information of leagues
        Steps:
        1.Create a webdriver instance
        2.Iterate through a list of available league urls
        2.1. Check results for new events
        2.2. Check fixtures
        2.3. Process data

        """
        pass

    @staticmethod
    def teams(self):
        """
        Process of information of leagues
        Steps:
        1.Create a webdriver instance
        2.Iterate through a list of available teams
        2.1. Check results for new events
        2.2. Check fixtures
        2.3. Process data
        
        """
        pass

def estimate_remaining_time(n, processed_elements, last_three_times):
    """estimate a remaininng time for a thread to finish its job
    Args:
        n: total number of urls to be processed
        processed_elements: number of urls currently processed
        last_three_times: time it took to complete the last three urls
    Returns:
        estimated remaining time
    """
    pass

if __name__ == "__main__":
    Basketball()