from selenium.webdriver.phantomjs import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver

from config import logger
from Collector import Collector
from Product import Product
import htmlTemplateService
from collectorService import get_soup_by_content, attribute_value_for_all_elements, all_href_urls, \
    inner_html, tags_text
from seleniumCollectorService import get_page_source_until_selector

BASE_URL = 'https://www.lwflooring.com/'
PRODUCTS_URL = BASE_URL + 'products.html'
LW_CSV_FILE_NAME = 'lw-hardwood-template.csv'

TIME_OUT_PRODUCT = 30
TIME_OUT_URL = 30

VENDOR_NAME = 'Lw Flooring'


def get_product_category_urls(driver: WebDriver, url: str):
    driver.get(url)
    page_content = get_page_source_until_selector(driver,
                                                  'img',
                                                  TIME_OUT_URL)
    soup = get_soup_by_content(page_content)
    category_urls = [BASE_URL + url for url in all_href_urls('#pu23978', soup)]
    category_urls.extend([BASE_URL + url for url in all_href_urls('#pu23981', soup)])
    return category_urls


def get_product_collectors_urls(driver: WebDriver, urls: []):
    collectors = []
    for url in urls:
        driver.get(url)
        page_content = get_page_source_until_selector(driver, '.nonblock', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        product_urls = attribute_value_for_all_elements('.clearfix.colelem.shared_content a', 'href', soup)
        collectors.extend(
            [Collector(BASE_URL + product_url, url.replace('.html', '').replace(BASE_URL, '')) for product_url in
             product_urls])
        logger.debug('Get this product urls: {} for category url: {}'.format(product_urls, url))
    return collectors


def get_all_products_details(driver: WebDriver, collectors: [Collector]):
    products = []
    id = 1
    for collector in collectors:
        logger.debug('Getting details for product url: {}'.format(collector.url))
        driver.get(collector.url)
        page_content = get_page_source_until_selector(driver,
                                                      '.PamphletWidget .nonblock.nontext.Container.museBGSize.grpelem.wp-panel.wp-panel-active',
                                                      TIME_OUT_PRODUCT)
        soup = get_soup_by_content(page_content)
        images = attribute_value_for_all_elements(
            '.PamphletWidget .nonblock.nontext.Container.museBGSize.grpelem.wp-panel.wp-panel-active', 'href', soup)
        main_image = BASE_URL + images[0]
        product_title = collector.url.replace('.html', '').replace(BASE_URL, '').title()

        labels_html = inner_html(
            '.shadow .clearfix.colelem > .clearfix.grpelem.shared_content:nth-child({})'.format(1), soup)
        labels = map(lambda v: v.replace(':', ''), tags_text('p', labels_html[0]))

        values_html = inner_html(
            '.shadow .clearfix.colelem > .clearfix.grpelem.shared_content:nth-child({})'.format(2), soup)
        values = tags_text('p', values_html[0])

        details = htmlTemplateService.create_product_template(labels, values)
        tags = ",".join(values)
        tags += ',' + collector.collection
        products.append(
            Product(product_title + str(id), main_image, '', product_title, VENDOR_NAME, '', '', details,
                    tags))
        id += 1
    return products


def get_products_details():
    driver = webdriver.WebDriver()
    category_urls = get_product_category_urls(driver, PRODUCTS_URL)
    products_collectors = get_product_collectors_urls(driver, category_urls)
    # TODO: remove bad links
    products_collectors = list(filter(lambda pc: '#' not in pc.url, products_collectors))
    products_collectors = list(filter(lambda pc: '---' not in pc.url, products_collectors))
    # ---
    products_collectors = list(dict.fromkeys(products_collectors))
    products_details = get_all_products_details(driver, products_collectors)
    driver.quit()
    return products_details
