import pytest
from selenium import webdriver
import time
#Provides webdriver object to the tests suite and is presisted for the entite session so that page does not have to be re-launched for each test.
page_url = ""
@pytest.yield_fixture(scope = 'session')
def driver():
    driver= webdriver.Chrome(r'C:\Users\Pawan\PycharmProjects\annalise\venv\utils\chromedriver.exe')
    time.sleep(3)
    yield driver
    time.sleep(3)
    driver.close()
