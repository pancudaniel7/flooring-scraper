import re

from selenium.webdriver.firefox.webdriver import WebDriver

import firefoxService
import htmlTemplateService
from Product import Product
from collectorService import get_soup_by_content, tag_text, \
    tags_text, all_href_urls, image_src, attribute_value_for_all_elements, attribute_value_element, inner_html, \
    inner_html_str
from config import logger
from seleniumCollectorService import get_page_source_until_selector_with_delay, get_page_source_until_selector

BASE_URL = 'https://shawfloors.com'
HARDWOOD_URL = BASE_URL + '/flooring/hardwood/'
CARPET_URL = BASE_URL + '/flooring/carpet/'
SHAW_HARDWOOD_CSV_FILE_NAME = 'shaw-hardwood-template.csv'
SHAW_CARPET_CSV_FILE_NAME = 'shaw-carpet-template.csv'

VENDOR_NAME = 'Shaw Flooring'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 120
TIME_DELAY = 1


def get_hardwood_category_urls(driver: WebDriver, url: str):
    product_category_urls = []
    driver.get(url)
    page_content = get_page_source_until_selector(driver, 'img', TIME_OUT_URL)
    soup = get_soup_by_content(page_content)
    last_page_number = int(re.sub(r'^([0-9]+ \/ )', '', tag_text(
        '#p_lt_ctl02_pageplaceholder_p_lt_ctl00_StyleCatalogFilter_paginationId > div.wrap > span', soup)))
    for page_number in range(1, last_page_number):
        logger.debug('Getting category urls for url: {}'.format(url + str(page_number)))
        driver.get(url + str(page_number))
        page_content = get_page_source_until_selector(driver, 'img', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        product_category_urls.extend(
            [BASE_URL + url for url in
             attribute_value_for_all_elements(
                 '#ProductData > div > div > div.swatch > div > div.view-details > label > a',
                 'href', soup)])
    return product_category_urls


def get_product_urls(driver: WebDriver, category_urls: []):
    product_urls = []
    for category_url in category_urls:
        logger.debug('Getting product urls for category url: {}'.format(category_url))
        driver.get(category_url)
        page_content = get_page_source_until_selector_with_delay(driver, 'img', TIME_OUT_URL, TIME_DELAY)
        soup = get_soup_by_content(page_content)
        product_urls.extend(all_href_urls('#scroller > li > ', soup))
    return product_urls


def get_all_products_details(driver: WebDriver, product_urls: []):
    products = []
    id = 1
    logger.debug('Products size: {}'.format(len(product_urls)))
    for product_url in product_urls:
        if id % 30 == 0:
            firefoxService.renew_session(driver)
        logger.debug('Getting details for product url: {}'.format(product_url))
        driver.get(product_url)
        page_content = get_page_source_until_selector_with_delay(driver,
                                                                 'img',
                                                                 TIME_OUT_URL, TIME_DELAY)
        soup = get_soup_by_content(page_content)
        title = tag_text('#sections > div > div > div > div > ul > li.box.box3.separator-left > span > h2',
                         soup).title()
        collection = tag_text('#sections > div > div > div > div > ul > li.box.box3.separator-left > h1', soup)
        product_type = tag_text('#sections > div > div > div > div > ul > li.box.box1.category.no-left', soup).title()
        image = attribute_value_element('#s7room_flyout > div.s7staticimage > img:nth-child(1)', 'src', soup)
        product_labels = tags_text('#specs-content-wrap > div > div > h3', soup)
        product_values = inner_html_str(
            '#specs-content-wrap > div > div.specs-content-cell:nth-child(2) > :not(.tooltip-wrap)', soup)
        product_values = list(map(lambda value: re.sub(r'<[^>]+>', '', value), product_values))
        details = htmlTemplateService.create_product_template(product_labels, product_values)
        tags = ','.join(product_values)
        tags += ',' + collection
        products.append(Product(title + str(id), image, '', title, VENDOR_NAME, '', product_type, details, tags))
        id += 1
    return products


def get_products_details(base_url):
    driver = firefoxService.renew_session()
    product_category_urls = get_hardwood_category_urls(driver, base_url)
    product_urls = get_product_urls(driver, product_category_urls)
    driver = firefoxService.renew_session(driver)
    products_details = get_all_products_details(driver, product_urls)
    driver.quit()
    return products_details
