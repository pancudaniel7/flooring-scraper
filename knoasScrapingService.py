import re

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

import htmlTemplateService
from Product import Product
from collectorService import get_soup_by_content, tag_text, \
    inner_html_str_index_0, tags_text, all_href_urls
from config import logger
from seleniumCollectorService import get_page_source_until_selector, get_page_source_until_selector_with_delay

BASE_URL = 'https://knoasflooring.com/product-category'
LAMINATE_URL = BASE_URL + '/laminate-floors'
VINYL_URL = BASE_URL + '/vinyl-floors'
WOOD_URL = BASE_URL + '/wood-floors'
ACCESSORIES_URL = BASE_URL + '/accessories'
KNOAS_CSV_FILE_NAME = 'knoas-hardwood-template.csv'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 120
TIME_DELAY = 1

VENDOR_NAME = 'Knoas Flooring'


def get_product_category_urls(driver: WebDriver, url: str):
    driver.get(url)
    page_content = get_page_source_until_selector(driver, '.entry-title', TIME_OUT_URL)
    soup = get_soup_by_content(page_content)
    return [url for url in all_href_urls('.woocom-list-content .entry-title', soup)]


def get_all_products_details(driver: WebDriver, product_urls: []):
    products = []
    for product_url in product_urls:
        logger.debug('Get details for product url: {}'.format(product_url))
        driver.get(product_url)
        page_content = get_page_source_until_selector_with_delay(driver,
                                                                 'img',
                                                                 TIME_OUT_URL, TIME_DELAY)
        soup = get_soup_by_content(page_content)
        collection = tag_text('.summary.entry-summary h1', soup)
        images = all_href_urls('.woocommerce-product-gallery__image ', soup)
        product_titles = list(
            map(lambda product_title: re.search(r'\/([0-9,a-z,A-Z,_,-]+?)\.(jpg|jpeg|png)$', product_title)
                .group(1).replace('_', ' ').title(), images))
        product_details = inner_html_str_index_0(
            '.woocommerce-Tabs-panel.woocommerce-Tabs-panel--description.panel.entry-content.wc-tab', soup).replace(
            '☛', '')
        soup = get_soup_by_content(product_details)
        product_details = tags_text('li', soup)

        if not product_details or product_details[0] == '':
            product_details = tags_text('p', soup)

        tags = ','.join(product_details)
        tags += ',' + collection
        id = 1
        for image, title in zip(images, product_titles):
            details = htmlTemplateService.create_second_product_template(product_details)
            products.append(Product(title + str(id), image, '', title, VENDOR_NAME, '', '', details, tags))
            id += 1
    return products


def get_products_details():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    product_collection_urls = get_product_category_urls(driver, LAMINATE_URL)
    product_collection_urls.extend(get_product_category_urls(driver, VINYL_URL))
    product_collection_urls.extend(get_product_category_urls(driver, WOOD_URL))
    # product_collection_urls.extend(get_product_category_urls(driver, ACCESSORIES_URL))
    products = get_all_products_details(driver, product_collection_urls)
    driver.quit()
    return products
