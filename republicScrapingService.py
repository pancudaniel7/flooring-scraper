import re

from selenium.webdriver.firefox.webdriver import WebDriver

import firefoxService
from Product import Product
from collectorService import get_soup_by_content
from collectorService import all_href_urls, all_images_src, tag_text
from config import logger
from seleniumCollectorService import get_page_source_until_selector

BASE_URL = 'https://www.republicfloor.com/'
LAMINATED_URL = BASE_URL + '/republic-products'
VINYL_1_URL = BASE_URL + '/republic-spc-products'
VINYL_2_URL = BASE_URL + '/copy-of-pure-spc-lvt'
REPUBLIC_LAMINATED_CSV_FILE_NAME = 'republic-laminated-template.csv'
REPUBLIC_VINYL_CSV_FILE_NAME = 'republic-vinyl-template.csv'

VENDOR_NAME = 'Republic Floor'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 500
TIME_DELAY = 1


def get_category_urls(driver: WebDriver, url: str):
    logger.debug('Getting category urls for: ' + url)
    driver.get(url)
    page_content = get_page_source_until_selector(driver, 'img', TIME_OUT_URL)
    soup = get_soup_by_content(page_content)
    return [url for url in all_href_urls('#c8n6inlineContent > div', soup)]


def get_collections_urls(driver: WebDriver, category_urls: []):
    product_collection_urls = []
    i = 0
    for category_url in category_urls:
        i += 1
        logger.debug(str(i) + '- Getting category url for: ' + category_url)
        driver.get(category_url)
        page_content = get_page_source_until_selector(driver, 'img', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        product_collection_urls.extend([url for url in all_href_urls('.mg1itemsContainer', soup)])
    return product_collection_urls


def get_product_urls(driver: WebDriver, collection_urls: []):
    print(collection_urls)
    product_urls = []
    i = 0
    for collection_url in collection_urls:
        i += 1
        logger.debug(str(i) + '- Getting product url for: ' + collection_url)
        driver.get(collection_url)
        page_content = get_page_source_until_selector(driver, 'img', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        product_urls.extend([replace_links(url.strip()) for url in all_href_urls('.mg1itemsContainer > div', soup)])
    return product_urls


def replace_links(link: ''):
    list_of_links = {
        'https://www.republicfloor.com/crystal-collection?lightbox=imagexqf': 'https://www.republicfloor.com/crystalclear-golden-walnut',
        'https://www.republicfloor.com/crystal-collection?lightbox=imagen12': 'https://www.republicfloor.com/crystalclear-wild-walnut',
        'https://www.republicfloor.com/crystal-collection?lightbox=image_wpq': 'https://www.republicfloor.com/crystalclear-patigonian-rosewood'
    }
    new_link = list_of_links.get(link, link)
    return new_link


def get_all_products_details(driver: WebDriver, collectors: [], type: str):
    products = []
    id = 0
    for collector in collectors:
        id += 1
        if id % 30 == 0:
            driver = firefoxService.renew_session(driver)
        logger.debug(str(id) + ' -Getting products details for product url: ' + collector)
        driver.get(collector)
        page_content = get_page_source_until_selector(driver, 'img', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        title = tag_text('* > p:nth-child(1) > span:nth-child(1) > span', soup).strip()
        image = all_images_src('.wp2link > .wp2img', soup)[1]
        try:
            product_details_search = \
                driver.find_elements_by_css_selector('.wp2link > .wp2img')[1].find_element_by_xpath(
                    './../../..').find_elements_by_css_selector('div')[4].find_element_by_css_selector('p > span')
            product_details_search = \
                driver.find_elements_by_css_selector('.wp2link > .wp2img')[1].find_element_by_xpath(
                    './../../..').find_elements_by_css_selector('div')[4]
        except Exception as e:
            product_details_search = \
                driver.find_elements_by_css_selector('.wp2link > .wp2img')[1].find_element_by_xpath(
                    './../../..').find_elements_by_css_selector('div')[7]
            logger.debug('*** problematic link resolved using second method on url: ' + collector + '\n' + str(e))
            pass
        products_details = product_details_search.get_attribute('innerHTML').replace('', '')
        tags = re.sub('(.*?):', '', product_details_search.get_attribute('innerText').replace('', '')).replace('.\n',
                                                                                                                ',').replace(
            '\n', ',')
        products.append(Product(title + str(id), image, '', title, VENDOR_NAME, '', type, products_details, tags))
        print('')
    return products


def get_products_details(base_url, type: str):
    driver = firefoxService.renew_session()
    product_category_urls = get_category_urls(driver, base_url)
    product_collection_urls = get_collections_urls(driver, product_category_urls)
    driver = firefoxService.renew_session(driver)
    product_urls = get_product_urls(driver, product_collection_urls)
    driver = firefoxService.renew_session(driver)
    products_details = get_all_products_details(driver, product_urls, type)
    driver.quit()
    return products_details
