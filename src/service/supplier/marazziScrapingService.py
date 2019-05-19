import re

from selenium.webdriver.firefox.webdriver import WebDriver

from config import logger
from model.Product import Product
from service.collector import collectorService
from service.collector.collectorService import get_soup_by_content, tag_text, tags_text, attribute_value_element
from service.collector.seleniumCollectorService import get_page_source_until_selector_with_delay
from service.html import htmlTemplateService
from service.session import firefoxService

BASE_URL = 'https://www.marazziusa.com'
TYPES_URL = BASE_URL + '/products'
MARAZZI_CSV_FILE_NAME = 'marazzi-hardwood-template.csv'
PRODUCT_TYPE = 'Tile'

TIME_OUT = 120
SLEEP_DELAY = 1

TIME_OUT_CLICK = 120
SLEEP_CLICK_DELAY = 1

VENDOR_NAME = 'Marazzi'


def get_all_products_details(driver: WebDriver, product_urls: []):
    products_details = []
    id = 1
    logger.debug('Product size: {} '.format(len(product_urls)))
    for url in product_urls:
        logger.debug('Collecting product details for url {}:{} '.format(id, url))
        if id % 5 == 0:
            driver = firefoxService.renew_session(driver)
        driver.get(url)
        page_content = get_page_source_until_selector_with_delay(driver, 'img', TIME_OUT, 0)
        soup = get_soup_by_content(page_content)

        image = attribute_value_element(
            '#node-image > img',
            'src', soup)
        product_title = tag_text('#node-info > h1', soup).replace('™', '').title()
        products_data = [re.sub(r'<[^>]+>', '', label) for label in
                         tags_text('#node-info > div', soup)]
        product_details = htmlTemplateService.create_second_product_template(products_data, '')
        tags = ','.join([re.sub(r'^(.*: *)', '', value) for value in products_data])
        products_details.append(
            Product(product_title + str(id), image, '', product_title,
                    VENDOR_NAME, '',
                    PRODUCT_TYPE, product_details,
                    tags))
        id += 1
    return products_details


def get_products_details():
    driver = firefoxService.renew_session()
    types_urls = collectorService.get_product_urls_for_pages(driver,
                                                             [TYPES_URL],
                                                             '#block-views-products-block > div > div > span > div > div > a',
                                                             TIME_OUT, 0)
    types_urls = [BASE_URL + url for url in types_urls]
    driver = firefoxService.renew_session(driver)
    collection_urls = collectorService.get_product_urls_for_pages(driver,
                                                                  types_urls,
                                                                  'div.image-container > a',
                                                                  TIME_OUT, 0)
    collection_urls = [BASE_URL + url for url in collection_urls]
    driver = firefoxService.renew_session(driver)
    product_urls = collectorService.get_product_urls_for_pages(driver,
                                                               collection_urls,
                                                               '#block-views-collections-block-3 > div > div > table > tbody > tr > td > div > a',
                                                               TIME_OUT, 0)
    product_urls = [BASE_URL + url for url in product_urls]
    driver = firefoxService.renew_session(driver)
    logger.debug('Number of products --->{}'.format(len(product_urls)))
    products_details = get_all_products_details(driver, product_urls)
    driver.quit()
    return products_details
