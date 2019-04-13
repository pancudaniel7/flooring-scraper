from selenium.webdriver.common.by import By
from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_page_source_until_selector(driver: WebDriver, selector: str, timeout: int = 10):
    WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
    return driver.page_source
