from selenium.webdriver.phantomjs import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver

from config import logger
from Product import Product
from collectorService import get_soup_by_content, all_attributes_for_all_elements, tags_text, \
    tag_text
from htmlTemplateService import create_second_product_template
from seleniumCollectorService import get_page_source_until_selector

BASE_URL = 'http://eaglecreekfloors.com/'

HARDWOOD_URL = BASE_URL + 'product-category/hardwood/?product_count=48'
LAMINATE_URL = BASE_URL + 'product-category/laminate/'
VINYL_URL = BASE_URL + 'product-category/luxury-vinyl/'

EAGLE_HARDWOOD_CSV_FILE_NAME = 'eagle-creek-hardwood-template.csv'
EAGLE_LAMINATE_CSV_FILE_NAME = 'eagle-creek-laminate-template.csv'
EAGLE_VINYL_CSV_FILE_NAME = 'eagle-creek-vinyl-template.csv'

TIME_OUT_PRODUCT = 30
TIME_OUT_URL = 50

VENDOR_NAME = 'Eagle Creek Flooring'


def get_product_urls(driver: WebDriver, url: str):
    driver.get(url)
    page_content = get_page_source_until_selector(driver,
                                                  '.hb-main-content .products a',
                                                  TIME_OUT_URL)
    soup = get_soup_by_content(page_content)
    category_urls = set(all_attributes_for_all_elements('.hb-main-content .products a', 'href', soup))
    return category_urls


def get_all_products_details(driver: WebDriver, urls: []):
    products = []
    id = 1
    for url in urls:
        logger.debug('Getting details for product url: {}'.format(url))
        driver.get(url)
        page_content = get_page_source_until_selector(driver,
                                                      '.woocommerce-product-gallery__wrapper a',
                                                      TIME_OUT_PRODUCT)
        soup = get_soup_by_content(page_content)
        image = all_attributes_for_all_elements(
            '.woocommerce-product-gallery__wrapper a', 'href', soup)[0]
        title = tag_text('.summary.entry-summary h3 span', soup).lower().title()
        product_code = tags_text('.sku_wrapper .sku', soup)[0]
        values = tags_text('.woocommerce-product-details__short-description td', soup)
        collection = values.pop(0).replace('Collection', '')
        details = create_second_product_template(values)
        tags = ",".join(values)
        tags += ',' + collection
        products.append(
            Product(title + str(id), image, '', title, VENDOR_NAME, product_code, '', details,
                    tags))
        id += 1
    return products


def get_hardwood_products_details():
    driver = webdriver.WebDriver()
    products_urls = get_product_urls(driver, HARDWOOD_URL)
    products_urls.remove('http://eaglecreekfloors.com/product-category/hardwood/wimberly/')
    products_urls.remove('http://eaglecreekfloors.com/product-category/hardwood/prestige-collection/')
    products_urls.remove('http://eaglecreekfloors.com/product-category/hardwood/windemere-collection/')
    products_urls.remove('http://eaglecreekfloors.com/product-category/hardwood/')
    products = get_all_products_details(driver, products_urls)
    driver.quit()
    return products


def get_laminate_products_details():
    driver = webdriver.WebDriver()
    products_urls = get_product_urls(driver, LAMINATE_URL)
    products_urls.remove('http://eaglecreekfloors.com/product-category/laminate/summit-collection/')
    products_urls.remove('http://eaglecreekfloors.com/products/oak-santana/')
    products_urls.remove('http://eaglecreekfloors.com/product-category/laminate/')
    products = get_all_products_details(driver, products_urls)
    driver.quit()
    return products


def get_vinyl_products_details():
    driver = webdriver.WebDriver()
    products_urls = get_product_urls(driver, VINYL_URL)
    products_urls.remove('http://eaglecreekfloors.com/product-category/luxury-vinyl/harbor-collection/')
    products_urls.remove('http://eaglecreekfloors.com/product-category/luxury-vinyl/lennox-collection/')
    products_urls.remove('http://eaglecreekfloors.com/product-category/luxury-vinyl/sinclair-collection/')
    products_urls.remove('http://eaglecreekfloors.com/product-category/luxury-vinyl/stonecrest-collection/')
    products_urls.remove('http://eaglecreekfloors.com/product-category/luxury-vinyl/')
    products = get_all_products_details(driver, products_urls)
    driver.quit()
    return products
