import re

from config import logger
from selenium.webdriver.firefox.webdriver import WebDriver

from model.Product import Product
from service.collector import collectorService
from service.collector.collectorService import get_soup_by_content, all_href_urls, tags_text, inner_html_str_index_0
from service.collector.seleniumCollectorService import get_page_source_until_selector_with_delay
from service.session import firefoxService

BASE_URL = 'https://www.fuzionflooring.com'
BISTRO_URL = BASE_URL + '/bistro-collection.html'
FUZION_CSV_FILE_NAME = 'fuzion-hardwood-template.csv'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 120
TIME_DELAY = 1

VENDOR_NAME = 'Fuzion Flooring'


def get_details(driver: WebDriver, url: str):
    products = []
    logger.debug('Get product details for url: {}'.format(url))
    driver.get(url)
    page_content = get_page_source_until_selector_with_delay(driver,
                                                             'img',
                                                             TIME_OUT_URL, TIME_DELAY)
    soup = get_soup_by_content(page_content)
    images = all_href_urls('.galleryInnerImageHolder ', soup)
    images = [BASE_URL + image for image in images]
    collections_titles = tags_text('.galleryCaptionInnerText', soup)
    collections = list(
        map(lambda collection: re.sub(r'\| .*$', '', collection).strip(),
            collections_titles))
    titles = list(
        map(lambda collection: re.sub(r'^.* \| ', '', collection).strip(),
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


def get_all_products_details(driver: WebDriver, product_urls: []):
    product_details = []
    logger.debug('Product url size: {}'.format(len(product_details)))
    id = 1
    for url in product_urls:
        if id % 10 == 0:
            driver = firefoxService.renew_session(driver)
        logger.debug('Getting product detail: {}'.format(str(id)))
        product_details.extend(get_details(driver, url))
    return list(set(product_details))


def get_product_details():
    driver = firefoxService.renew_session()
    types_urls = ['https://www.fuzionflooring.com/engineered-hardwood.html',
                  'https://www.fuzionflooring.com/luxury-vinyl.html', 'https://www.fuzionflooring.com/laminate.html',
                  'https://www.fuzionflooring.com/carpet-tile.html']
    collection_urls = collectorService.get_product_urls_for_pages(driver, types_urls,
                                                                  'div.imageGallery > div > div > div > div > div > a',
                                                                  TIME_OUT_URL, 0)
    collection_urls = [BASE_URL + url for url in collection_urls]
    driver = firefoxService.renew_session(driver)
    products = get_all_products_details(driver, collection_urls)
    driver.quit()
    return products
