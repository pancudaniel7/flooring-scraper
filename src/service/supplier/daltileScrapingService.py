import re

from selenium.webdriver.firefox.webdriver import WebDriver

from config import logger
from model.Product import Product
from service.collector import collectorService
from service.collector.collectorService import get_soup_by_content, tag_text, all_href_urls, \
    attribute_value_for_all_elements, tags_text
from service.collector.seleniumCollectorService import get_page_source_after_click_with_delay, \
    get_page_source_until_selector_with_delay
from service.html import htmlTemplateService
from service.session import firefoxService

BASE_URL = 'https://www.daltile.com'
COLLECTIONS_URL = BASE_URL + '/collections'
DALTILE_CSV_FILE_NAME = 'daltile-hardwood-template.csv'
PRODUCT_TYPE = 'Tile'

TIME_OUT = 120
SLEEP_DELAY = 1

TIME_OUT_CLICK = 120
SLEEP_CLICK_DELAY = 1

VENDOR_NAME = 'Daltile Hardwood Flooring'


def get_collection_urls(driver: WebDriver, category_base_url: str):
    driver.get(category_base_url)
    page_content = get_page_source_until_selector_with_delay(driver,
                                                             'img', TIME_OUT, SLEEP_DELAY)
    soup = get_soup_by_content(page_content)
    collection_pages_number = int(
        tag_text('span.currentPagesCount', soup).strip())
    logger.debug('Collection pages number:{} '.format(collection_pages_number))

    collections_urls = []
    collections_urls.extend(all_href_urls('#updateContent > div > div > div > div', soup))
    for counter in range(1, collection_pages_number):
        logger.debug('Getting collections urls for page number {}:{} '.format(counter, category_base_url))
        page_content = get_page_source_after_click_with_delay(driver,
                                                              'body > div:nth-child(10) > div > div.container > div > div.col-md-9 > div:nth-child(3) > div > nav > ul > li:nth-child(4) > a',
                                                              TIME_OUT_CLICK, SLEEP_CLICK_DELAY)
        soup = get_soup_by_content(page_content)
        collections_urls.extend(all_href_urls('#updateContent > div > div > div > div', soup))

    return set(BASE_URL + url for url in collections_urls)


def get_all_products_details(driver: WebDriver, product_urls: []):
    products_details = []
    id = 1
    logger.debug('Product size: {} '.format(len(product_urls)))
    for url in product_urls:
        logger.debug('Collecting product details for url {}:{} '.format(id, url))
        if id % 1 == 0:
            driver = firefoxService.renew_session(driver)
        driver.get(url)
        page_content = get_page_source_until_selector_with_delay(driver, 'img', TIME_OUT, SLEEP_DELAY)
        soup = get_soup_by_content(page_content)

        images = attribute_value_for_all_elements(
            'body div.slider-image-nav.slick-initialized.slick-slider > div > div > div > img',
            'src', soup)
        image = images[0] if len(images) > 0 else ''
        product_title = tag_text('body > div.breadcrumb-banner > h2', soup)
        product_labels = [re.sub(r'<[^>]+>', '', label) for label in
                          tags_text('body div.product-information__table > div > div:nth-child(1)', soup)]
        product_values = [re.sub(r'<[^>]+>', '', label) for label in
                          tags_text('body div.product-information__table > div > div:nth-child(2)', soup)]
        product_values[1] = '_'
        product_details = htmlTemplateService.create_product_template(product_labels, product_values, '')
        collection = tag_text('body > div.breadcrumb-banner > div > div > span:nth-child(3) > a', soup)

        tags = ','.join([re.sub(r' {3,}', '', value) for value in product_values])
        tags += ',' + collection
        products_details.append(
            Product(product_title + str(id), image, '', product_title,
                    VENDOR_NAME, '',
                    PRODUCT_TYPE, product_details,
                    tags))
        id += 1
    return list(set(products_details))


def get_products_details():
    driver = firefoxService.renew_session()
    category_urls = get_collection_urls(driver, COLLECTIONS_URL)
    driver = firefoxService.renew_session(driver)
    product_urls = collectorService.get_product_urls_for_pages(driver,
                                                               list(category_urls),
                                                               '#products-in-series > div > div > a',
                                                               TIME_OUT, SLEEP_DELAY)
    product_urls = [BASE_URL + url for url in product_urls]
    driver = firefoxService.renew_session(driver)
    products_details = get_all_products_details(driver, product_urls)
    driver.quit()
    return products_details
