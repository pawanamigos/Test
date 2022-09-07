from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time

#Since I coulkd not get the server running and cannot access the webpage, I have detaled the process I would follow to create E2E tests with placehlders for element locators.
page_url = ""
add_image_locator = ""
image_id_locator = ""
add_image_tag_locator = ""
image_name_locator = ""
created_date_locator = ""
delete_image_locator = ""
delete_tag_locator = ""
add_image_name_locator = ""
add_image_button_locator = ""
image_locator = ""
tag_locator = ""


def launch_product_page(driver):
    driver.get(page_url)
    time.sleep(3)
    assert driver.current_url == "page url"


def add_image_and_details(driver):
    driver.find_element(By.XPATH,add_image_locator).click()
    time.sleep(2)
    driver.find_element(By.XPATH, add_image_name_locator).send_keys("Image name")
    time.sleep(2)
    driver.find_element(By.XPATH, add_image_tag_locator).send_keys("tag name")
    time.sleep(2)
    driver.find_element(By.XPATH, add_image_button_locator).click()
    try:
        driver.find_element(By.XPATH, image_locator)
        image_added = True
    except NoSuchElementException as e:
        image_added = False
    assert driver.find_element(By.XPATH, image_name_locator).text == "Image name"
    assert driver.find_element(By.XPATH, tag_locator).text == "tag name"
    assert image_added == True








