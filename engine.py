import utils

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

import re
import tempfile
from datetime import datetime

from webdriver_manager.chrome import ChromeDriverManager #this library automatically downloads the latest version of chrome webdriver so that i do not have to manually download a new version everything that chrome get an update


class engine:
    def __init__(self):
        pass