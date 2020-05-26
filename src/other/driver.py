from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from env_utils.base_dir import base_dir


class SelfCloseableWebdriver:
    def __init__(self):
        _options = Options()
        _options.headless = True
        self.driver = webdriver.Chrome(executable_path=f"{base_dir}/third parties/chromedriver.exe", options=_options)

    def __del__(self):
        self.driver.quit()


_self_closeable_webdriver = SelfCloseableWebdriver()

driver = _self_closeable_webdriver.driver
