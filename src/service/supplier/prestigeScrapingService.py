import re

from selenium.webdriver.firefox.webdriver import WebDriver

from config import logger
from model.Product import Product
from service.collector import collectorService
from service.collector.collectorService import get_soup_by_content, tag_text, tags_text, \
    attribute_value_for_all_elements
from service.collector.seleniumCollectorService import get_page_source_until_selector_with_delay
from service.html import htmlTemplateService
from service.session import firefoxService

BASE_URL = 'https://bpiprestige.com'
PRESTIGE_CSV_FILE_NAME = 'prestige-template.csv'

TIME_OUT = 120
SLEEP_DELAY = 1

TIME_OUT_CLICK = 120
SLEEP_CLICK_DELAY = 1

VENDOR_NAME = 'Prestige'


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

        images = attribute_value_for_all_elements(
            '#product-all-images > div > div > div > div > div.grid-view-item__image-wrapper.product-card__image-wrapper.box.ratio-container.js.lazyloaded',
            'style', soup)
        images = ['https:' + re.search(r'\((.*)\)', img).group(1) for img in images]
        collection = tag_text('#product-all-images > div > div > div > div > div.product-details > h4:nth-child(1)',
                              soup).replace('Collection: ', '').title()
        titles = [title.replace('Color: ', '') for title in
                  tags_text('#product-all-images > div > div > div > div > div.product-details > h4:nth-child(2)',
                            soup)]
        product_codes = [product_code.replace('Item Number: ', '') for product_code in tags_text(
            '#product-all-images > div > div > div > div > div.product-details > h4:nth-child(3)',
            soup)]
        product_type = tag_text(
            '#ProductSection-product-template > div.grid.product-single > div.grid__item.medium-up--one-half.product-single__meta-wrapper.tooshort > div > div > div > h2 > a',
            soup).title()

        products_data = [re.sub(r'<[^>]+>', '', label) for label in
                         tags_text(
                             'form.product-form > div.product-single__description.rte > ul > li',
                             soup)]

        for image, title, product_code in zip(images, titles, product_codes):
            product_details = htmlTemplateService.create_second_product_template(products_data, product_code)
            tags = ','.join([re.sub(r'^(.*: *)', '', value) for value in products_data])
            products_details.append(
                Product(title + str(id), image, '', title,
                        VENDOR_NAME, '',
                        product_type, product_details,
                        tags))
        id += 1
    return products_details


def get_products_details():
    driver = firefoxService.renew_session()
    types_urls = collectorService.get_product_urls_for_pages(driver,
                                                             [BASE_URL],
                                                             '#shopify-section-1541104687899 > div > div > div > div > a',
                                                             TIME_OUT, 0)
    types_urls = [BASE_URL + url for url in types_urls]
    driver = firefoxService.renew_session(driver)
    collection_urls = collectorService.get_product_urls_for_pages(driver,
                                                                  types_urls,
                                                                  '#Collection > div > div > div > a',
                                                                  TIME_OUT, 0)
    collection_urls = [BASE_URL + url for url in collection_urls]
    driver = firefoxService.renew_session(driver)
    products_details = get_all_products_details(driver, collection_urls)
    driver.quit()
    return products_details
