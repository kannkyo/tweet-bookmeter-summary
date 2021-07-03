
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


def open_bookmeter_summary(driver: webdriver, user_id: str, order: str = "desc", insert_break: bool = True, image_size: str = "medium"):
    driver.get(
        f"https://bookmeter.com/users/{user_id}/summary/yearly/posting/bookmeter")


def tweet_summary(driver: webdriver):
    summary_button: WebElement = driver.find_element_by_xpath(
        '//*[@class="content__btn"]')
    summary_button.click()

    tweet_modal_window: WebElement = driver.find_element_by_xpath(
        '//*[@class="controller__button"]')
    tweet_modal_window.submit()
