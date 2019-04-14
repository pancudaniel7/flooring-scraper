from selenium.webdriver.phantomjs import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver

from src.config import logger
from src.model.Product import Product
from src.service.common import htmlTemplateService
from src.service.common.collectorService import get_soup_by_content, tag_text, \
    all_attributes_for_all_elements, inner_html_str_index_0, tags_text, all_href_urls
from src.service.common.seleniumCollectorService import get_page_source_until_selector

BASE_URL = 'https://knoasflooring.com/product-category'
LAMINATE_URL = BASE_URL + '/laminate-floors'
VINYL_URL = BASE_URL + '/vinyl-floors'
WOOD_URL = BASE_URL + '/wood-floors'
ACCESSORIES_URL = BASE_URL + '/accessories'
KNOAS_CSV_FILE_NAME = 'knoas-hardwood-template.csv'

TIME_OUT_PRODUCT_DELAY = 4
TIME_OUT_URL_DELAY = 120

VENDOR_NAME = 'Knoas Flooring'


def get_product_category_urls(driver: WebDriver, url: str):
    driver.get(url)
    page_content = get_page_source_until_selector(driver, '.entry-title', TIME_OUT_URL_DELAY)
    soup = get_soup_by_content(page_content)
    return [url for url in all_href_urls('.woocom-list-content .entry-title', soup)]


def get_all_products_details(driver: WebDriver, product_urls: []):
    products = []
    for product_url in product_urls:
        logger.debug('Get details for product url: {}'.format(product_url))
        driver.get(product_url)
        page_content = get_page_source_until_selector(driver,
                                                      'img',
                                                      TIME_OUT_URL_DELAY)
        soup = get_soup_by_content(page_content)
        images = all_attributes_for_all_elements('.flex-control-nav.flex-control-thumbs img', 'src', soup)
        collection = tag_text('.summary.entry-summary h1', soup)
        product_titles = all_attributes_for_all_elements('.woocommerce-product-gallery__image a img', 'title', soup)
        product_details = inner_html_str_index_0(
            '.woocommerce-Tabs-panel.woocommerce-Tabs-panel--description.panel.entry-content.wc-tab', soup).replace(
            '☛', '')
        soup = get_soup_by_content(product_details)
        product_details = tags_text('li', soup)
        if not product_details or product_details[0] == '':
            product_details = tags_text('p', soup)
        tags = ",".join(product_details)
        tags += ',' + collection
        details = htmlTemplateService.create_second_product_template(product_details)
        id = 1
        for image, title in zip(images, product_titles):
            products.append(Product(title + str(id), image, '', title, VENDOR_NAME, '', '', details, tags))
            id += 1
    return products


def get_products_details():
    driver = webdriver.WebDriver()
    product_collection_urls = get_product_category_urls(driver, LAMINATE_URL)
    product_collection_urls.extend(get_product_category_urls(driver, VINYL_URL))
    product_collection_urls.extend(get_product_category_urls(driver, WOOD_URL))
    # product_collection_urls.extend(get_product_category_urls(driver, ACCESSORIES_URL))
    products = get_all_products_details(driver, product_collection_urls)
    driver.quit()
    return products
