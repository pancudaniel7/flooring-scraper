import re

from selenium.webdriver.phantomjs import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver

from src.config import logger
from src.model.Product import Product
from src.service.common import htmlTemplateService
from src.service.common.collectorService import get_soup_by_content, all_href_urls, tag_text, \
    tags_text, all_attributes_for_all_elements
from src.service.common.seleniumCollectorService import get_page_source_until_selector, \
    get_page_source_after_click_with_delay, get_page_source_until_selector_with_delay

BASE_URL = 'https://www.mullicanflooring.com'
PRODUCTS_URL = BASE_URL + '/Products'
SUK_URL = BASE_URL + '/Product-Detail?sku='
MULLICAN_CSV_FILE_NAME = 'mullican-hardwood-template.csv'

TIME_OUT_PRODUCT = 10
TIME_OUT_CLICK = 10
SLEEP_CLICK_DELAY = 2
SLEEP_DELAY = 1

VENDOR_NAME = 'Mullican Hardwood Flooring'


def get_product_urls(driver: WebDriver, product_url: str):
    driver.get(product_url)
    page_content = get_page_source_until_selector(driver,
                                                  '#vue-productListing > div:nth-child(2) > div > h1', TIME_OUT_PRODUCT)
    soup = get_soup_by_content(page_content)
    products_size = int(
        tag_text('#vue-productListing > div:nth-child(2) > div > h1', soup).replace('products', '').strip())

    for counter in range(0, int(products_size / 9)):
        page_content = get_page_source_after_click_with_delay(driver, '.g-hover-cursor-pointer',
                                                              TIME_OUT_CLICK, SLEEP_CLICK_DELAY)

    soup = get_soup_by_content(page_content)
    product_urls = all_href_urls(
        '#vue-productListing > div:nth-child(3) > div > div > div > div > div > ',
        soup)
    logger.debug('Collected {} main product urls: '.format(products_size))
    return set(map(lambda url: BASE_URL + url, product_urls))


def get_sub_product_urls(driver: webdriver, product_urls: []):
    sub_product_urls = []
    for url in product_urls:
        logger.debug('Collecting sub product urls for url: {}'.format(url))
        driver.get(url)
        page_content = get_page_source_until_selector(driver, '#vue-product-detail img',
                                                      TIME_OUT_PRODUCT)
        soup = get_soup_by_content(page_content)
        product_codes = set(all_attributes_for_all_elements(
            '#vue-product-detail > div:nth-child(2) > div > div> div > img', 'src', soup))
        sub_product_urls.extend(list(map(
            lambda product_code: SUK_URL + re.search(r'/([0-9]{1,5})-', product_code).group(1) if re.search(
                r'/([0-9]{1,5})-',
                product_code) else False,
            product_codes)))
    return list(filter(lambda url: url != False, sub_product_urls))


def get_all_products_details(driver: WebDriver, product_urls: []):
    products_details = []
    id = 1
    for url in product_urls:
        logger.debug('Collecting product details for url: {} with number: {}'.format(url, id))
        driver.get(url)
        page_content = get_page_source_until_selector_with_delay(driver, '#vue-product-detail td', TIME_OUT_PRODUCT,
                                                                 SLEEP_DELAY)
        soup = get_soup_by_content(page_content)

        images = all_attributes_for_all_elements(
            '#vue-product-detail > div:nth-child(2) > div > img', 'src', soup)
        if len(images) == 0:
            continue
        image = BASE_URL + images[0]
        product_title = tag_text('#vue-product-detail > div:nth-child(2) > div:nth-child(2) > h1', soup)
        product_code = url.replace(SUK_URL, '')
        labels = tags_text('#vue-product-detail tbody tr td:nth-child(1)', soup)
        labels.pop(0)
        values = tags_text('#vue-product-detail tbody tr td:nth-child(2)', soup)
        collection = values.pop(0)
        product_details = htmlTemplateService.create_product_template(labels, values, product_code)
        tags = ','.join(values)
        tags += ',' + collection
        products_details.append(
            Product(product_title + str(id), image, '', product_title,
                    VENDOR_NAME, product_code,
                    '', product_details,
                    tags))
        id += 1
    return products_details


def get_products_details():
    driver = webdriver.WebDriver()
    product_urls = get_product_urls(driver, PRODUCTS_URL)
    all_products_urls = get_sub_product_urls(driver, product_urls)
    products_details = get_all_products_details(driver, all_products_urls)
    driver.quit()
    return products_details
