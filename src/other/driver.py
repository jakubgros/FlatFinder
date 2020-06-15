from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager


class SelfCloseableWebdriver:
    def __init__(self):
        _options = Options()
        _options.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=_options)

    def __del__(self):
        self.driver.close()


_self_closeable_webdriver = SelfCloseableWebdriver()

driver = _self_closeable_webdriver.driver
