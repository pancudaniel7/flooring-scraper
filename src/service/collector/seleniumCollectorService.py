import time

from selenium.webdriver.common.by import By
from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_page_source_until_selector(driver: WebDriver, selector: str, timeout: int = 10):
    WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
    return driver.page_source


def get_page_source_until_selector_with_delay(driver: WebDriver, selector: str, timeout: int = 10, delay_time: int = 2):
    WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
    time.sleep(delay_time)
    return driver.page_source


def get_page_source_after_click(driver: WebDriver, selector: str, timeout: int = 10):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
    return driver.page_source


def get_page_source_after_click_with_delay(driver: WebDriver, selector: str, timeout: int = 10, delay_time: int = 2):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
    time.sleep(delay_time)
    return driver.page_source

def get_page_source_after_click_by_javascript(driver: WebDriver, selector: str, timeout: int = 10):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    driver.execute_script('arguments[0].click();', element)
    return driver.page_source


def get_page_source_after_click_by_javascript_with_delay(driver: WebDriver, selector: str, timeout: int = 10,
                                                         delay_time: int = 2):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    driver.execute_script('arguments[0].click();', element)
    time.sleep(delay_time)
    return driver.page_source
