from selenium.webdriver.phantomjs import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver

from src.Config import logger
from src.service.common.CollectorService import get_soup_by_page_content, all_href_urls
from src.service.common.SeleniumCollectorService import get_page_source_until_selector

BASE_URL = 'https://www.mohawkflooring.com'
CARPET_URL = BASE_URL + '/carpet/search?page='
WOOD_URL = BASE_URL + '/wood/search?page='
VINYL_URL = BASE_URL + '/vinyl/search?page='
TILE_URL = BASE_URL + '/tile/search?page='
RUGS_URL = BASE_URL + '/rugs/search?page='

VENDOR_NAME = 'Mohawk Flooring'
CARPET_CSV_FILE_NAME = 'mohawk-flooring-carpet-template.csv'
WOOD_CSV_FILE_NAME = 'mohawk-flooring-wood-template.csv'

TIME_OUT_DYNAMIC_DELAY = 2


def get_product_categories_urls_for_page(driver: WebDriver, url: str, page_number: int):
    try:
        driver.get(url + str(page_number))
        page_source = get_page_source_until_selector(driver, '.product-image', TIME_OUT_DYNAMIC_DELAY)
        soup = get_soup_by_page_content(page_source)
        return [BASE_URL + url for url in all_href_urls('.style-tile', soup)]
    except Exception as e:
        logger.debug('Did not find any page source on page: {} with exception: {}'.format(page_number, e))
        return None


def get_all_product_category_urls(driver: WebDriver, url: str):
    category_urls = []
    i = 1
    while True:
        response = get_product_categories_urls_for_page(driver, url, i)
        if response is None:
            return category_urls
        i += 1
        category_urls.extend(response)


def get_product_urls(driver: WebDriver, category_urls: []):
    products_urls = []
    for category_url in category_urls:
        pass


def get_wood_products_details():
    driver = webdriver.WebDriver()
    category_urls = get_all_product_category_urls(driver, WOOD_URL)

    driver.quit()
    return None
