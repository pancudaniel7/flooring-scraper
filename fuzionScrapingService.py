import re

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

import htmlTemplateService
from Product import Product
from collectorService import get_soup_by_content, inner_html_str_index_0, tags_text, all_href_urls
from config import logger
from seleniumCollectorService import get_page_source_until_selector_with_delay

BASE_URL = 'https://www.fuzionflooring.com'
BISTRO_URL = BASE_URL + '/bistro-collection.html'
FUZION_CSV_FILE_NAME = 'fuzion-hardwood-template.csv'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 120
TIME_DELAY = 1

VENDOR_NAME = 'Fuzion Flooring'


def get_all_products_details(driver: WebDriver, url: str):
    products = []
    logger.debug('Get all product details for url: {}'.format(url))
    driver.get(url)
    page_content = get_page_source_until_selector_with_delay(driver,
                                                             'img',
                                                             TIME_OUT_URL, TIME_DELAY)
    soup = get_soup_by_content(page_content)
    images = all_href_urls('.galleryInnerImageHolder ', soup)
    images = [BASE_URL + image for image in images]
    collections_titles = tags_text('.galleryCaptionInnerText', soup)
    collections = list(
        map(lambda collection: re.search(r'^([A-Z,a-z,0-9, ]+)\|([A-Z,a-z,0-9, ]+)$', collection).group(1).strip(),
            collections_titles))
    titles = list(
        map(lambda collection: re.search(r'^([A-Z,a-z,0-9, ]+)\|([A-Z,a-z,0-9, ]+)$', collection).group(2).strip(),
            collections_titles))
    product_details = inner_html_str_index_0(
        '#wsite-content > div:nth-child(1) > div > div > div > div > div.paragraph', soup) \
        .replace('<br/><br/>', '<br/>').replace('•', '')
    tags = re.sub(r'<[^>]+>', '', product_details)
    tags = ','.join(re.findall(r'(\w+)', tags))
    id = 1
    for image, collection, title in zip(images, collections, titles):
        products.append(
            Product(title + str(id), image, '', title, VENDOR_NAME, '', '', product_details, tags + ',' + collection))
        id += 1
    return products


def get_products_details():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    products = get_all_products_details(driver, BISTRO_URL)
    driver.quit()
    return products
