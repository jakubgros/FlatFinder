from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager


class SelfCloseableWebdriver:
    def __init__(self):
        _options = Options()
        _options.headless = True
        _options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=_options)

    def __del__(self):
        self.driver.close()


_self_closeable_webdriver = SelfCloseableWebdriver()

driver = _self_closeable_webdriver.driver
