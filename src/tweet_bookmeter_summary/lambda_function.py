import logging
import os
import time
import traceback
from datetime import datetime
from dateutil.relativedelta import relativedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

import bookmeter_login_page
import bookmeter_summary_page
import secret

level = os.environ.get('LOG_LEVEL', 'INFO')


def logger_level():
    if level == 'CRITICAL':
        return 50
    elif level == 'ERROR':
        return 40
    elif level == 'WARNING':
        return 30
    elif level == 'INFO':
        return 20
    elif level == 'DEBUG':
        return 10
    else:
        return 0


logger = logging.getLogger()
logger.setLevel(logger_level())


def tweet_summary(driver: webdriver, user_info: dict):
    HOME_BASE_URL = "https://bookmeter.com/home/"

    # Open Login Site
    driver.get(HOME_BASE_URL)

    # Login
    bookmeter_login_page.login(
        driver=driver,
        username=user_info['name'],
        password=user_info['password'])

    # Open Summary Page
    bookmeter_summary_page.open_bookmeter_summary(
        driver=driver, user_id=user_info['id'])

    bookmeter_summary_page.tweet_summary(driver=driver)


def chrome_driver():
    options = Options()
    options.binary_location = "/opt/python/bin/headless-chromium"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(
        executable_path="/opt/python/bin/chromedriver",
        chrome_options=options)

    return driver


def lambda_handler(event, context):
    logger.debug(event)

    try:
        region_name = "ap-northeast-1"

        secret_bookmeter = secret.get_secret(
            region_name=region_name,
            secret_name=os.environ.get('BOOKMETER_SECRET_NAME'))

        driver = chrome_driver()

        tweet_summary(driver=driver, user_info=secret_bookmeter)

        # Wait
        time.sleep(1)

        # Exit
        driver.quit()

        return {
            'statusCode': "ok"
        }

    except Exception as e:
        logger.error(traceback.format_exc())
        raise e
