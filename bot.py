import utils
from multiprocessing import Pool
import time

class Basketball:
    def __init__(self):

        self.URLS = utils.load_json("urls.json")
        self.SETTINGS = utils.load_json("settings.json")
        if not all([self.URLS, self.SETTINGS]):
            raise RuntimeError("Critical error: IMPORTANT DATA NOT LOADED INTO MEMORY. Execution halted.")
        
        self.file_handler_args = (
            self.SETTINGS["Path"],
            self.SETTINGS["Defaults"]["create_keys"],
            self.SETTINGS["Defaults"]["data_encoding"],
        )
    
    def run(self):
        """Execution Logic"""
        if self.SETTINGS["Actions"]["Scrape_league"]:
            print("League Job Started")
        
        params = (
            self.SETTINGS["Defaults"]["Headless"],
            self.SETTINGS["Defaults"]["Timeout"],
            self.SETTINGS["Defaults"]["Load_Page_Attempts"],
            self.URLS["Homepage"],
        )

        threads = self.SETTINGS["Defaults"]["Threads"]

        urls = list(self.URLS["Leagues"].values())
        league_chunks = self.split_into_n_chunks(urls, threads)

        tasks = [
            (i, chunk_urls, self.file_handler_args, self.SETTINGS, params)
            for i, chunk_urls in enumerate(league_chunks)
        ]

        with Pool(processes=threads) as pool:
            pool.starmap(Basketball.leagues, tasks)

    def split_into_n_chunks(self, lst, n):
        k, m = divmod(len(lst), n)
        return [
            lst[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)
        ]

    @staticmethod
    def leagues(thread_num: int,urls: list, file_handler_args: tuple, SETTINGS: dict, params: tuple,):
        """
        Process of information of leagues
        Steps:
        1.Create a webdriver instance
        2.Iterate through a list of available league urls
        2.1. Check results for new events
        2.2. Check fixtures
        2.3. Process data
        """
        from engine import engine
        from files import FileHandler

        data = FileHandler(*file_handler_args)
        webdriver = engine(*params)

        print(f"Thread: {thread_num}")

        event_urls = set() # i am going to use hashtable as it is easier for comparisons i.e checking if something is already inside O(1)
        fixtures_urls = set()

        # get links to all results and fixtures
        for url in urls:
            print(f"URL: {url}")

            if webdriver.load_url(url+"results/") and webdriver.check_results():
                while not webdriver.scroll(direction=0, knots=SETTINGS["Defaults"]["scroll"]):

                    events = webdriver.return_results()
                    for event in events:
                        try:
                            link = webdriver.get_url(event)
                            if link:
                                event_urls.add(link)

                        except Exception as e:
                            continue
                    print(f"\rurls found: {len(event_urls)}", end="", flush=True)
            print()
                        
            if webdriver.load_url(url+"fixtures/") and webdriver.check_results():
                while not webdriver.scroll(direction=0, knots=SETTINGS["Defaults"]["scroll"]):
                    
                    events = webdriver.return_results()
                    for event in events:
                        try:

                            link = webdriver.get_url(event)
                            if link:
                                fixtures_urls.add(link)

                        except Exception as e:
                            continue
                    print(f"\rurls found: {len(fixtures_urls)}", end="", flush=True)
            print()

        for event in event_urls:
            webdriver.load_url(event)
            print(webdriver.format_match_info(webdriver.get_match_info().text))
            print(webdriver.format_match_scores(webdriver.get_match_scores().text))

if __name__ == "__main__":
    bot = Basketball()
    bot.run()