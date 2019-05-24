from selenium.webdriver.firefox.webdriver import WebDriver

from config import logger
from model.Product import Product
from service.collector import collectorService
from service.collector.collectorService import get_soup_by_content, tag_text, tags_text, \
    attribute_value_element
from service.collector.seleniumCollectorService import get_page_source_until_selector_with_delay
from service.html import htmlTemplateService
from service.session import firefoxService
from selenium.webdriver.firefox.webdriver import WebDriver

from config import logger
from model.Product import Product
from service.collector import collectorService
from service.collector.collectorService import get_soup_by_content, tag_text, tags_text, \
    attribute_value_element
from service.collector.seleniumCollectorService import get_page_source_until_selector_with_delay
from service.html import htmlTemplateService
from service.session import firefoxService

BASE_URL = 'https://www.urbanfloor.com'
PRODUCTS_URL = BASE_URL + '/All_products.html'
URBAN_CSV_FILE_NAME = 'urban-hardwood-template.csv'
PRODUCT_TYPE = 'Hardwood'

TIME_OUT = 120
SLEEP_DELAY = 0

TIME_OUT_CLICK = 120
SLEEP_CLICK_DELAY = 1

VENDOR_NAME = 'Urban'


def get_all_products_details(driver: WebDriver, product_urls: []):
    products_details = []
    id = 1
    logger.debug('Product size: {} '.format(len(product_urls)))
    for url in product_urls:
        logger.debug('Collecting product details for url {}:{} '.format(id, url))
        if id % 5 == 0:
            driver = firefoxService.renew_session(driver)
        driver.get(url)
        page_content = get_page_source_until_selector_with_delay(driver, 'img', TIME_OUT, SLEEP_DELAY)
        soup = get_soup_by_content(page_content)

        image = attribute_value_element(
            '#main-content > div.p-detail > div.p-detail-tum > div > div > div.col-xs-12.col-sm-4 > a',
            'href', soup)
        collection = tag_text(
            '#main-content > div.p-detail > div.p-detail-top > div > div > div > div.col-xs-12.col-sm-12.col-lg-6.col-lg-offset-3.ac > div > p > a',
            soup).title()
        title = tag_text(
            '#main-content > div.p-detail > div.p-detail-top > div > div > div > div.col-xs-12.col-sm-12.col-lg-6.col-lg-offset-3.ac > div > h1',
            soup)

        labels = [label.replace(':', '').title() for label in tags_text(
            '#tabs-main-2 > div:nth-child(2) > div.row.info-table-liine > div > table > tbody > tr > td:nth-child(1)',
            soup)]
        values = [value for value in tags_text(
            '#tabs-main-2 > div:nth-child(2) > div.row.info-table-liine > div > table > tbody > tr > td:nth-child(2)',
            soup)]
        product_details = htmlTemplateService.create_product_template(labels, values)
        tags = ','.join(values) + ',' + collection
        products_details.append(
            Product(title + str(id), image, '', title, VENDOR_NAME, '', PRODUCT_TYPE, product_details, tags))
        id += 1
    return list(set(products_details))


def get_products_details():
    driver = firefoxService.renew_session()
    collection_urls = collectorService.get_product_urls_for_pages(driver,
                                                                  [PRODUCTS_URL],
                                                                  '#main-content > div.p-index-main > div.container-fluid > div > div > div > a',
                                                                  TIME_OUT, SLEEP_DELAY)
    driver = firefoxService.renew_session(driver)
    products_details = get_all_products_details(driver, collection_urls)
    driver.quit()
    return products_details
