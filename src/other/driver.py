from selenium import webdriver

from env_utils.base_dir import base_dir

driver = webdriver.Chrome(executable_path=f"{base_dir}/third parties/chromedriver.exe")
