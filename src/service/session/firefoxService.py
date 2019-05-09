from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver


def renew_session(driver: WebDriver = None, options: webdriver.FirefoxOptions = None):
    if driver is not None:
        driver.quit()
    if options is None:
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        return webdriver.Firefox(options=options)
    return webdriver.Firefox(options=options)
