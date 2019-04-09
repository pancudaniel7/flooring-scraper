from selenium.webdriver.phantomjs import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver

from src.Config import logger
from src.service.common.CollectorService import get_soup_by_content, all_href_urls
from src.service.common.SeleniumCollectorService import get_page_source_until_selector

BASE_URL = 'http://www.regalhardwoods.com'
CATEGORIES_URL = BASE_URL + '/floors'
REGAL_CSV_FILE_NAME = 'mohawk-flooring-wood-template.csv'

TIME_OUT_DYNAMIC_DELAY = 2
TIME_OUT_PRODUCT_DELAY = 4
TIME_OUT_URL_DELAY = 5


def get_product_category_urls_per_page(driver: WebDriver, url: str):
    try:
        driver.get(url)
        page_content = get_page_source_until_selector(driver, '.mask', TIME_OUT_URL_DELAY)
        soup = get_soup_by_content(page_content)
        return [BASE_URL + url for url in all_href_urls('.brand-items .mask', soup)]
    except Exception as e:
        logger.debug(
            'Did not find any page source for the page:'.format(BASE_URL + url, e))
        return None


def get_product_urls(driver: WebDriver, category_urls: []):
    products_urls = []
    try:
        for category_url in category_urls:
            driver.get(category_url)
            page_content = get_page_source_until_selector(driver, '.mask', TIME_OUT_URL_DELAY)
            soup = get_soup_by_content(page_content)
            products_urls.extend([BASE_URL + url for url in all_href_urls('.brand-items .mask', soup)])
    except Exception as e:
        logger.error(
            'Fail to get product urls with message: {}'.format(e))
        return None
    return products_urls


def get_products_details():
    driver = webdriver.WebDriver()
    category_urls = get_product_category_urls_per_page(driver, CATEGORIES_URL)
    product_urls = get_product_urls(driver, category_urls)
    driver.quit()
    return None
