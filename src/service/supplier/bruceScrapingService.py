import re

from selenium.webdriver.firefox.webdriver import WebDriver

from service.collector.collectorService import get_soup_by_content, attribute_value_for_all_elements, all_href_urls, \
    tag_text, attribute_value_element, tags_text, image_src
from service.session import firefoxService
from service.html import htmlTemplateService
from model.Product import Product

from config import logger
from service.collector.seleniumCollectorService import get_page_source_until_selector

BASE_URL = 'http://www.bruce.com'
HARDWOOD_URL = BASE_URL + '/flooring/hardwood/_/N-67o/No-'
BRUCE_CSV_FILE_NAME = 'bruce-hardwood-template.csv'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 120
TIME_DELAY = 1

VENDOR_NAME = 'Bruce Flooring'


def get_hardwood_category_urls(driver: WebDriver, url: str):
    product_category_urls = []
    counter_number = 80
    for page_number in range(1, 15):
        logger.debug('Getting category urls for url: {}'.format(url + str(counter_number)))
        driver.get(url + str(counter_number))
        counter_number += 16  # page counter number iteration is 16
        page_content = get_page_source_until_selector(driver, 'img', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        product_category_urls.extend(
            [BASE_URL + url for url in
             attribute_value_for_all_elements(
                 '#mainContents > div.content > div.products > div.gridItem > p > a:first-child', 'href', soup)])
    return product_category_urls


def get_product_urls(driver: WebDriver, category_urls: []):
    product_urls = []
    id = 1
    for category_url in category_urls:
        if id % 20 == 0:
            logger.debug('Renew the driver session')
            driver = firefoxService.renew_session(driver)
        logger.debug('Getting product urls for category url: {}'.format(category_url))
        driver.get(category_url)
        page_content = get_page_source_until_selector(driver, '#colors div a', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        product_urls.append(driver.current_url)
        product_urls.extend([BASE_URL + url for url in all_href_urls('#colors div ', soup)])
        id += 1
    return product_urls


def get_all_products_details(driver: WebDriver, product_urls: []):
    products = []
    id = 1
    logger.debug('Products size: {}'.format(len(product_urls)))
    for product_url in product_urls:
        logger.debug('Getting details for product url: {}'.format(product_url))
        if id % 20 == 0:
            logger.debug('Renew the driver session')
            driver = firefoxService.renew_session(driver)
        driver.get(product_url)
        page_content = get_page_source_until_selector(driver,
                                                      'img',
                                                      TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        title = tag_text('#mainContents > div.titleHeaderTrans > div:nth-child(2) > h1', soup)
        product_type = re.sub(r'^([0-9] [a-z]+\.)', '',
                              tag_text('#mainContents > div.titleHeaderTrans > div:nth-child(2) > h2', soup)).strip()
        image = attribute_value_element('#hardwoodRoomM > img.rs.swatch.ui-draggable', 'src', soup)
        product_labels = tags_text('#floorOverview > div.col-left > table > tbody tr th', soup)
        product_values = tags_text('#floorOverview > div.col-left > table > tbody tr td', soup)
        details = htmlTemplateService.create_product_template(product_labels, product_values)
        tags = ','.join(product_values)
        tags += ',' + product_values[3]
        products.append(Product(title + str(id), image, '', title, VENDOR_NAME, '', product_type, details, tags))
        id += 1
    return products


def get_products_details():
    driver = firefoxService.renew_session()
    product_category_urls = get_hardwood_category_urls(driver, HARDWOOD_URL)
    product_urls = get_product_urls(driver, product_category_urls)
    product_urls = set(product_urls)
    driver = firefoxService.renew_session(driver)
    products_details = get_all_products_details(driver, product_urls)
    products_details = set(products_details)
    driver.quit()
    return set(products_details)
