import re

from selenium.webdriver.firefox.webdriver import WebDriver
from config import logger
from model.Product import Product
from service.collector.collectorService import get_soup_by_content, tag_text, all_href_urls, tags_text
from service.session import firefoxService
from service.supplier.seleniumCollectorService import get_page_source_until_selector
from service.html import htmlTemplateService

BASE_URL = 'https://residential.tarkett.com'
LAMINATED_URL = BASE_URL + '/en_US/category-tna_R01044-laminate?tab=PRODUCTS'
VINYL_1_URL = BASE_URL + '/en_US/category-tna_R01014-vinyl-sheet?tab=PRODUCTS'
VINYL_2_URL = BASE_URL + '/en_US/category-tna_R01021-luxury-vinyl-tiles-and-planks?tab=PRODUCTS'
CARPET_URL = BASE_URL + '/en_US/category-tna_R01018-modular?tab=PRODUCTS'
TARKETT_LAMINATED_CSV_FILE_NAME = 'tarkett-laminated-template.csv'
TARKETT_VINYL_CSV_FILE_NAME = 'tarkett-vinyl-template.csv'
TARKETT_CARPET_CSV_FILE_NAME = 'tarkett-carpet-template.csv'

VENDOR_NAME = 'Tarkett'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 1500
TIME_DELAY = 1


def get_number_of_pages(driver: WebDriver, url: str):
    logger.debug('Getting category urls for: ' + url)
    driver.get(url)
    page_content = get_page_source_until_selector(driver,
                                                  'li.image-link-sku__item:nth-child(1) > div:nth-child(1) > figure:nth-child(1) > a',
                                                  TIME_OUT_URL)
    soup = get_soup_by_content(page_content)
    last_page_number = 1
    if soup.find('.tksb-pagination>div:nth-last-child(2)') != None:
        last_page_number = int(tag_text('.tksb-pagination>div:nth-last-child(2)', soup))
    return last_page_number


def get_products_url(driver: WebDriver, number_of_pages, initial_url: str):
    products_url = []
    i = 0
    for page_number in range(1, number_of_pages + 1):
        i += 1
        page_url = initial_url + '&page=' + str(page_number)
        logger.debug(str(i) + '- Getting product url for: ' + page_url)
        driver.get(page_url)
        page_content = get_page_source_until_selector(driver,
                                                      'li.image-link-sku__item:nth-child(1) > div:nth-child(1) > figure:nth-child(1) > a:nth-child(1)',
                                                      TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        products_url.extend([BASE_URL + url.strip() for url in all_href_urls('li.image-link-sku__item', soup)])
    return products_url


def get_all_products_details(driver: WebDriver, products_url: [], type: str):
    products = []
    id = 0
    for product_url in products_url:
        id += 1
        if id % 30 == 0:
            driver = firefoxService.renew_session(driver)
        logger.debug(str(id) + ' -Getting products details for product url: ' + product_url)
        driver.get(product_url)
        page_content = get_page_source_until_selector(driver, '.sku-hero__background-img', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        title = tag_text('span.tksb-icon-breadcrumb__label', soup).strip().title()
        collection = tag_text('a.tksb-icon-breadcrumb__label', soup).strip().title()
        image = soup.find('div', {'class': 'sku-hero__background-img'})['data-imgsmall']
        product_labels = tags_text('#accordion-common-attributes-tab-0 > div:nth-child(1) > table > tbody > tr > th',
                                   soup)
        product_values = tags_text(
            '#accordion-common-attributes-tab-0 > div:nth-child(1) > table > tbody > tr > td:nth-child(3)', soup)
        product_ids = tags_text('div.format-list__format-item-container > div > div > div > span', soup)
        if len(product_values) < 2:
            tags = product_values[0]
        else:
            tags = ','.join(product_values)
        tags += ',' + collection
        for product_id in product_ids:
            details = htmlTemplateService.create_product_template(product_labels, product_values, product_id)
            products.append(Product(title + str(id), image, '', title, VENDOR_NAME, '', type, details, tags))

    return products


def get_products_details(base_url, type: str):
    driver = firefoxService.renew_session()
    number_of_pages = get_number_of_pages(driver, base_url)
    product_urls = get_products_url(driver, number_of_pages, base_url)
    driver = firefoxService.renew_session(driver)
    products_details = get_all_products_details(driver, product_urls, type)
    driver.quit()
    return products_details
