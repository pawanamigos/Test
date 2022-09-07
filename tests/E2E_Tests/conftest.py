import pytest
from selenium import webdriver
import time

page_url = ""
@pytest.yield_fixture(scope = 'class')
def driver():
    driver= webdriver.Chrome(r'C:\Users\Pawan\PycharmProjects\annalise\venv\utils\chromedriver.exe')
    time.sleep(3)
    yield driver
    time.sleep(3)
    driver.close()
