import re

from config import logger
from selenium.webdriver.firefox.webdriver import WebDriver

from model.Product import Product
from service.collector.collectorService import get_soup_by_content, attribute_value_for_all_elements, tag_text, \
    all_href_urls, inner_html, attribute_value_element, tags_text, inner_html_str
from service.html import htmlTemplateService
from service.session import firefoxService
from service.supplier.seleniumCollectorService import get_page_source_until_selector, \
    get_page_source_until_selector_with_delay
from service.url import urlFileService

BASE_URL = 'https://shawfloors.com'
HARDWOOD_URL = BASE_URL + '/flooring/hardwood/'
CARPET_URL = BASE_URL + '/flooring/carpet/'

SHAW_HARDWOOD_CSV_FILE_NAME = 'shaw-hardwood-template.csv'
SHAW_CARPET_CSV_FILE_NAME = 'shaw-carpet-template.csv'
SHAW_CARPET_URL_FILE_NAME = 'shaw-carpet-url.txt'

VENDOR_NAME = 'Shaw Flooring'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 120
TIME_DELAY = 1


def get_hardwood_category_urls(driver: WebDriver, url: str):
    product_category_urls = []
    driver.get(url)
    page_content = get_page_source_until_selector(driver, 'img', TIME_OUT_URL)
    soup = get_soup_by_content(page_content)
    last_page_number = int(re.sub(r'^([0-9]+ \/ )', '', tag_text(
        '#p_lt_ctl02_pageplaceholder_p_lt_ctl00_StyleCatalogFilter_paginationId > div.wrap > span', soup)))
    for page_number in range(1, last_page_number):
        logger.debug('Getting category urls for url: {}'.format(url + str(page_number)))
        driver.get(url + str(page_number))
        page_content = get_page_source_until_selector(driver, 'img', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        product_category_urls.extend(
            [BASE_URL + url for url in
             attribute_value_for_all_elements(
                 '#ProductData > div > div > div.swatch > div > div.view-details > label > a',
                 'href', soup)])
    return product_category_urls


def get_product_urls(driver: WebDriver, category_urls: []):
    product_urls = []
    id = 1
    logger.debug('Products category url size: {}'.format(len(category_urls)))
    for category_url in category_urls:
        if id % 100 == 0:
            driver = firefoxService.renew_session(driver)
        logger.debug('Getting product urls for category url {}:{}'.format(id, category_url))
        driver.get(category_url)
        page_content = get_page_source_until_selector_with_delay(driver, 'img', TIME_OUT_URL, TIME_DELAY)
        soup = get_soup_by_content(page_content)
        product_urls.extend(all_href_urls('#scroller > li > ', soup))
        id += 1
    return product_urls


def get_all_products_details(driver: WebDriver, product_urls: []):
    products = []
    try:
        id = 1
        logger.debug('Products size: {}'.format(len(product_urls)))
        for product_url in product_urls:
            if id % 100 == 0:
                driver = firefoxService.renew_session(driver)
            logger.debug('Getting details for product url {}:{}'.format(id, product_url))
            driver.get(product_url)
            page_content = get_page_source_until_selector_with_delay(driver,
                                                                     'img',
                                                                     TIME_OUT_URL, TIME_DELAY)
            soup = get_soup_by_content(page_content)
            title = tag_text('#sections > div > div > div > div > ul > li.box.box3.separator-left > span > h2',
                             soup).title()
            collection = tag_text('#sections > div > div > div > div > ul > li.box.box3.separator-left > h1', soup)
            product_type = tag_text('#sections > div > div > div > div > ul > li.box.box1.category.no-left',
                                    soup).title()

            product_code = inner_html('#sections > div > div > div > div > ul > li.box.box2', soup)
            product_code = product_code[0].next.replace(
                'Style No.', '').replace('\r', '').replace('\n', '').strip() if len(product_code) > 0 else ''

            image = attribute_value_element('#s7room_flyout > div.s7staticimage > img:nth-child(1)', 'src', soup)

            product_labels = tags_text('#specs-content-wrap > div > div > h3', soup)
            product_values = inner_html_str(
                '#specs-content-wrap > div > div.specs-content-cell:nth-child(2) > :not(.tooltip-wrap)', soup)
            product_values = list(map(lambda value: re.sub(r'<[^>]+>', '', value), product_values))
            details = htmlTemplateService.create_product_template(product_labels, product_values)
            tags = ','.join(product_values)
            tags += ',' + collection
            products.append(
                Product(title + str(id), image, '', title, VENDOR_NAME, product_code, product_type, details, tags))
            id += 1
    except Exception as e:
        logger.debug('Exception message: {}'.format(e))
    return products


def get_products_details(base_url: str, product_urls_number: int = 9999, counter: int = 0,
                         product_url_file_path: str = ''):
    driver = firefoxService.renew_session()
    if urlFileService.is_url_file_empty(product_url_file_path):
        product_category_urls = get_hardwood_category_urls(driver, base_url)
        product_urls = get_product_urls(driver, product_category_urls)
        product_urls = set(product_urls)
        product_urls = list(product_urls)
        urlFileService.write_url_list_to_file(product_url_file_path, product_urls)
    else:
        first_index = product_urls_number * counter
        last_index = first_index + product_urls_number
        product_urls = urlFileService.read_url_list_from_file(product_url_file_path)[first_index:last_index]

    driver = firefoxService.renew_session(driver)
    products_details = get_all_products_details(driver, product_urls[:product_urls_number])
    driver.quit()
    return products_details
