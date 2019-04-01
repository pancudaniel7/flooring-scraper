from selenium.webdriver.phantomjs import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver

from src.Config import logger
from src.service.common.CollectorService import get_soup_by_page_content, all_href_urls, \
    all_attributes_for_all_elements, tag_text, tags_text
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
        page_content = get_page_source_until_selector(driver, '.product-image', TIME_OUT_DYNAMIC_DELAY)
        soup = get_soup_by_page_content(page_content)
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


def get_category_product_url(driver: WebDriver, category_url: str):
    driver.get(category_url)
    page_content = get_page_source_until_selector(driver, '#related-color', TIME_OUT_DYNAMIC_DELAY)
    soup = get_soup_by_page_content(page_content)
    data_style_ids = all_attributes_for_all_elements('.slider-container div>a', 'data-style-id', soup)
    data_color_ids = all_attributes_for_all_elements('.slider-container div>a', 'data-color-id', soup)
    product_category_title = tag_text('.column.main-info h2', soup).replace(' ', '-')
    products_tiles = [text.replace(' ', '-') for text in tags_text('.slider-container span[class^="ng-binding"]', soup)]
    return None


def get_product_urls(driver: WebDriver, category_urls: []):
    products_urls = []
    for category_url in category_urls:
        pass


def get_wood_products_details():
    driver = webdriver.WebDriver()
    # category_urls = get_all_product_category_urls(driver, WOOD_URL)
    get_category_product_url(driver,
                             'https://www.mohawkflooring.com/engineered-wood/detail/370-2291/Brookedale-Soft-Scrape-Uniclic-Cognac-Maple')
    driver.quit()
    return None
