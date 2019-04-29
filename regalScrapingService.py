import re

from config import logger
from selenium.webdriver.phantomjs import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver

import htmlTemplateService
from Collector import Collector
from Product import Product
from collectorService import get_soup_by_content, all_href_urls, tag_text, \
    inner_html_str_index_0, tags_text, extract_product_details_from_html
from seleniumCollectorService import get_page_source_until_selector

BASE_URL = 'http://www.regalhardwoods.com'
CATEGORIES_URL = BASE_URL + '/floors'
REGAL_CSV_FILE_NAME = 'regal-hardwood-template.csv'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 5

VENDOR_NAME = 'Regal Flooring'


def get_product_category_urls(driver: WebDriver, url: str):
    logger.debug('Getting category urls for: ' + url)
    driver.get(url)
    page_content = get_page_source_until_selector(driver, '.mask', TIME_OUT_URL)
    soup = get_soup_by_content(page_content)
    return [BASE_URL + url for url in all_href_urls('.brand-items .mask', soup)]


def get_product_urls(driver: WebDriver, category_urls: []):
    products_urls = []
    for category_url in category_urls:
        logger.debug('Getting products urls for category url: ' + category_url)
        driver.get(category_url)
        page_content = get_page_source_until_selector(driver, '.mask', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        product_collection = re.search(r'\/([0-9,a-z,A-Z,-]+)$', category_url).group(1).replace('-', ' ').title()
        products_urls.extend(
            [Collector(BASE_URL + url, product_collection) for url in all_href_urls('.brand-items .mask', soup)])
    return products_urls


def get_all_products_details(driver: WebDriver, collectors: []):
    products_details = []
    id = 1
    for collector in collectors:
        logger.debug('Getting products details for product url: ' + collector.url)
        driver.get(collector.url)
        page_content = get_page_source_until_selector(driver, '.mask', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)

        # TODO: Refactor image size, the size exeedes the 20 mb limit
        # first_image = all_attributes_for_all_elements('.floor-visual.box .bg-cover', 'style', soup)[0].replace(
        #     'background-image:url(', '').replace(');', '')
        # second_image = all_attributes_for_all_elements(
        #     '.box.floor-slideshow.slideshow.gallery-js-ready.autorotation-disabled .bg-cover', 'style', soup)[
        #     0].replace('background-image:url(', '').replace(');', '')

        product_title = tag_text('.slide .text-holder h1', soup).title()
        product_details = inner_html_str_index_0('.box .info-list', soup)
        product_details_fields = extract_product_details_from_html(product_details, '.name',
                                                                   '.value')
        product_details = htmlTemplateService.create_product_template(product_details_fields[0],
                                                                      product_details_fields[1]).replace('::',
                                                                                                         ':')
        tags = ','.join(tags_text('.value', soup))
        tags += ',' + collector.product_collection
        products_details.append(
            Product(product_title + str(id), '', '', product_title, VENDOR_NAME, '', '', product_details,
                    tags))
        id += 1
    return products_details


def get_products_details():
    driver = webdriver.WebDriver()
    category_urls = get_product_category_urls(driver, CATEGORIES_URL)
    product_urls = get_product_urls(driver, category_urls)
    products_details = get_all_products_details(driver, product_urls)
    driver.quit()
    return products_details
