import re

from selenium.webdriver.firefox.webdriver import WebDriver

from service.session import firefoxService
from service.html import htmlTemplateService
from model.Product import Product
from service.collector.collectorService import get_soup_by_content
from service.collector.collectorService import all_href_urls, all_images_src, tag_text, href_url_index_0
from config import logger
from service.collector.seleniumCollectorService import get_page_source_until_selector, \
    get_page_source_until_selector_with_delay
from service.url import urlFileService

BASE_URL = 'https://www.republicfloor.com/'
LAMINATED_URL = BASE_URL + 'republic-products'
VINYL_URL = BASE_URL + 'republic-spc-products'
LAMINATED_CSV_FILE_NAME = 'republic-laminated-template.csv'
VINYL_CSV_FILE_NAME = 'republic-vinyl-template.csv'
LAMINATED_URL_FILE_NAME = 'republic-laminated-url.txt'
VINYL_URL_FILE_NAME = 'republic-vinyl-url.txt'

VENDOR_NAME = 'Republic Floor'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 700
TIME_DELAY = 4


def get_category_urls(driver: WebDriver, url: str):
    logger.debug('Getting category urls for: ' + url)
    driver.get(url)
    page_content = get_page_source_until_selector(driver, 'img', TIME_OUT_URL)
    soup = get_soup_by_content(page_content)
    if url.endswith('republic-products'):
        return [url for url in all_href_urls('#c8n6inlineContent > div', soup)]
    elif url.endswith('republic-spc-products'):
        return [url for url in all_href_urls('#z4mmbinlineContent>.wp1>', soup)]


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
        if id % 10 == 0:
            driver = firefoxService.renew_session(driver)
        logger.debug(str(id) + ' -Getting products details for product url: ' + collector)
        driver.get(collector)
        page_content = get_page_source_until_selector_with_delay(driver, '.wp2link > .wp2img > img', TIME_DELAY)
        soup = get_soup_by_content(page_content)

        if soup.find('div', {'class': 's_VzqUUImageZoomSkinimageItem_meta'}) is not None:
            collector = href_url_index_0('.s_VzqUUImageZoomSkinimageItem_meta>', soup)
            logger.debug(str(id) + ' -Getting products details for product new url: ' + collector)
            driver.get(collector)
            page_content = get_page_source_until_selector_with_delay(driver, '.wp2link > .wp2img > img', TIME_DELAY)
            soup = get_soup_by_content(page_content)

        title = tag_text('* > p:nth-child(1) > span:nth-child(1) > span', soup).strip()
        image = re.sub(r'.jpg.*', '.jpg', all_images_src('main>div>div>div>div>div>div>div>div', soup)[0] )
        collection = re.sub(r'\b(?:collection|Collection|COLLECTION)\b', '',
                            tag_text('* > p:nth-child(1) > span:nth-child(2) > span', soup)).replace('(', '').replace(
            ')', '').strip()
        product_details_search = driver.find_elements_by_css_selector('.wp2link > .wp2img')[1].find_element_by_xpath(
            './../../..').find_elements_by_css_selector('div')
        try:
            product_details_search = product_details_search[4].find_element_by_css_selector('p').text.replace('', '')
        except Exception as e:
            product_details_search = product_details_search[7].text.replace('', '')
            logger.debug('*** problematic link resolved using second method on url: ' + collector + '\n' + str(e))
            pass
        product_labels = re.sub(r':.*', '', product_details_search).split('\n')
        product_values = re.sub(r'(.*?):', '', product_details_search).split('\n')
        product_values = list(map(lambda value: re.sub(r'\.$', '', value), product_values))
        details = htmlTemplateService.create_product_template(product_labels, product_values)
        tags = ','.join(product_values)
        tags += ',' + collection
        products.append(Product(title + str(id), image, '', title, VENDOR_NAME, '', type, details, tags))
    return products


def get_products_details(base_url, type: str, product_url_file_path: str = ''):
    driver = firefoxService.renew_session()
    if urlFileService.is_url_file_empty(product_url_file_path):
        product_category_urls = get_category_urls(driver, base_url)
        product_collection_urls = get_collections_urls(driver, product_category_urls)
        product_urls = get_product_urls(driver, product_collection_urls)
        urlFileService.write_url_list_to_file(product_url_file_path, product_urls)
    else:
        product_urls = urlFileService.read_url_list_from_file(product_url_file_path)
    driver = firefoxService.renew_session(driver)
    products_details = get_all_products_details(driver, product_urls, type)
    driver.quit()
    return products_details
