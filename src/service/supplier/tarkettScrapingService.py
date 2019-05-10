import re

from selenium.webdriver.firefox.webdriver import WebDriver
from config import logger
from bs4 import BeautifulSoup
from service.collector.collectorService import get_soup_by_content, tag_text, all_href_urls
from service.session import firefoxService
from service.supplier.republicScrapingService import replace_links
from service.supplier.seleniumCollectorService import get_page_source_until_selector

BASE_URL = 'https://residential.tarkett.com/en_US'
LAMINATED_URL = BASE_URL + '/search/products?search[body]=&filter-category_b2c%5B%5D=Laminate'
VINYL_URL = BASE_URL + '/category-tna_R01014-vinyl-sheet?tab=PRODUCTS'
CARPET_URL = BASE_URL + '/copy-of-pure-spc-lvt'
TARKETT_LAMINATED_CSV_FILE_NAME = 'tarkett-laminated-template.csv'
TARKETT_VINYL_CSV_FILE_NAME = 'tarkett-vinyl-template.csv'
TARKETT_CARPET_CSV_FILE_NAME = 'tarkett-carpet-template.csv'

VENDOR_NAME = 'Tarkett'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 500
TIME_DELAY = 1


def get_number_of_pages(driver: WebDriver, url: str):
    # url = 'https://residential.tarkett.com/en_US/category-tna_R01014-vinyl-sheet?tab=PRODUCTS'
    logger.debug('Getting category urls for: ' + url)
    driver.get(url)
    page_content = get_page_source_until_selector(driver, '.tksb-pagination>div:nth-last-child(2)', TIME_OUT_URL)
    soup = get_soup_by_content(page_content)
    last_page_number = int(tag_text('.tksb-pagination>div:nth-last-child(2)', soup))
    return last_page_number


def get_product_urls(driver: WebDriver, number_of_pages: int):
    product_urls = []
    i = 0
    for page in range(1, number_of_pages):
        i += 1
        url = driver.current_url
        # logger.debug(str(i) + '- Getting product url for: ' + collection_url)
        # driver.get(collection_url)
        page_content = get_page_source_until_selector(driver, 'img', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        product_urls.extend([replace_links(url.strip()) for url in all_href_urls('.mg1itemsContainer > div', soup)])
    return product_urls

def get_products_details(base_url, type: list):
    driver = firefoxService.renew_session()
    number_of_pages = get_number_of_pages(driver, base_url)
    product_urls = get_product_urls(driver, number_of_pages)

    driver.quit()
    return product_urls
