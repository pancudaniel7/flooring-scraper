from telnetlib import EC

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from config import logger
from model.Product import Product
from service.collector.collectorService import get_soup_by_content, tag_text, all_href_urls, tags_text, href_url_index_0
from service.session import firefoxService
from service.collector.seleniumCollectorService import get_page_source_until_selector_with_delay
from service.html import htmlTemplateService
from service.url import urlFileService

BASE_URL = 'http://www.eleganzatiles.com/product-series/'
TILE_URLS = ['ceramic-tiles.html', 'porcelain.html', 'glass-tiles.html', 'thin-tiles.html', 'thick-tiles.html']
TILE_CSV_FILE_NAME = 'eleganza-tile-template.csv'
TILE_URL_FILE_NAME = 'eleganza-tile-url.txt'
BAD_URLS = [
    'http://www.eleganzatiles.com/catalog/product/view/id/2525/s/precious-marble-bianco-oro-36x36-matte/category/163/']

VENDOR_NAME = 'Eleganza'

TIME_OUT_PRODUCT = 20
TIME_OUT_URL = 1500
TIME_DELAY = 3


def get_group_urls(driver: WebDriver, urls: list):
    group_urls = []
    for url in urls:
        new_url = BASE_URL + url

        while True:
            logger.debug('Getting category urls for: ' + new_url)
            driver.get(new_url)
            page_content = get_page_source_until_selector_with_delay(driver, 'div.margin-image', TIME_DELAY)
            soup = get_soup_by_content(page_content)
            group_urls.extend(all_href_urls('div.nova-product-images>', soup))

            if soup.find('a', {'class': 'i-next'}) is None:
                break
            else:
                new_url = all_href_urls('.pages>ol>li:last-child', soup)[1]

    return group_urls


def get_products_urls(driver: WebDriver, products_urls: list):
    all_products_url = []

    for url in products_urls:
        logger.debug('Getting products url for: ' + url)
        driver.get(url)
        page_content = get_page_source_until_selector_with_delay(driver, '.nova-product-images', TIME_DELAY)
        soup = get_soup_by_content(page_content)
        all_products_url.extend(all_href_urls('div.nova-product-images>div.margin-image>', soup))

    return all_products_url


def get_all_products_details(driver: WebDriver, products_url: [], type: str):
    driver.set_page_load_timeout(TIME_OUT_PRODUCT)
    for bad_url in BAD_URLS:
        if bad_url in products_url:
            products_url.remove(bad_url)
    products = []
    id = 0
    for product_url in products_url:
        page_not_found = False
        id += 1
        if id % 10 == 0:
            driver = firefoxService.renew_session(driver)
        logger.debug('Getting products details for product url {}:{} '.format(id, product_url))
        try:
            driver.get(product_url)
            page_content = get_page_source_until_selector_with_delay(driver, '#image-zoom', TIME_DELAY)
        except selenium.common.exceptions.TimeoutException:
            logger.debug('Possible bad url, skipping: ' + product_url)
            page_not_found = True
            pass
        if page_not_found == True:
            continue
        soup = get_soup_by_content(page_content)
        title = tag_text('.product-name > h1', soup).strip().title()
        image = href_url_index_0('#wrap', soup)
        product_labels = tags_text('tr > th.label:nth-child(1) > span', soup)
        product_values = tags_text('tr > td', soup)
        tags = ','.join(product_values)
        details = htmlTemplateService.create_product_template(product_labels, product_values)
        products.append(Product(title + ' ' + str(id), image, '', title, VENDOR_NAME, '', type, details, tags))

    return products


def get_products_details(url_list, type: str, product_url_file_path: str = ''):
    driver = firefoxService.renew_session()

    if urlFileService.is_url_file_empty(product_url_file_path):
        group_urls = get_group_urls(driver, url_list)
        products_url = get_products_urls(driver, group_urls)
        urlFileService.write_url_list_to_file(product_url_file_path, products_url)
    else:
        products_url = urlFileService.read_url_list_from_file(product_url_file_path)
    driver = firefoxService.renew_session(driver)
    products_details = get_all_products_details(driver, products_url, type)
    driver.quit()
    return products_details
