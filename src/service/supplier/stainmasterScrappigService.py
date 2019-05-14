import re
from selenium.webdriver.firefox.webdriver import WebDriver
from config import logger
from model.Product import Product
from service.collector.collectorService import get_soup_by_content, tag_text, all_href_urls, tags_text, image_src
from service.session import firefoxService
from service.collector.seleniumCollectorService import get_page_source_until_selector, get_page_source_after_click
from service.html import htmlTemplateService
from time import sleep
from service.url import urlFileService

BASE_URL = 'https://www.stainmaster.com'
CARPET_URL = BASE_URL + '/carpet/products/allcarpets/'
VINYL_1_URL = BASE_URL + '/vinyl/products/allvinyls/'
STAINMASTER_CARPET_CSV_FILE_NAME = 'stainmaster-carpet-template.csv'
STAINMASTER_VINYL_CSV_FILE_NAME = 'stainmaster-vinyl-template.csv'
VENDOR_NAME = 'StainMaster'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 5000
TIME_DELAY = 1


def get_products_url(driver: WebDriver, url: str):
    products_url = []
    logger.debug('Getting pages number from: ' + url)
    driver.get(url)
    page_content = get_page_source_until_selector(driver, '.pagination > li:nth-child(5) > a', TIME_OUT_URL)
    get_page_source_after_click(driver, '.pagination > li:nth-child(5) > a', TIME_OUT_URL)
    page_content = get_page_source_until_selector(driver,
                                                  'div.col-xs-6 > div:nth-child(1) > div:nth-child(2) > a:nth-child(3)',
                                                  TIME_OUT_URL)
    soup = get_soup_by_content(page_content)
    number_of_pages = int(tags_text('li.ng-scope:nth-child(5) > a:nth-child(1)', soup)[1].strip())
    for page_number in range(1, number_of_pages + 1):
        url = url + '?pageNumber=' + str(page_number) + '&productSelect=20&Favorites=false'
        logger.debug(str(page_number) + '- Getting product url for: ' + url)
        driver.get(url)
        page_content = get_page_source_until_selector(driver,
                                                      'div.col-xs-6 > div:nth-child(1) > div:nth-child(2) > a:nth-child(3)',
                                                      TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        products_url.extend([BASE_URL + url.strip() for url in all_href_urls('div.row:nth-child(5)', soup)])

    return products_url


def get_all_products_details(driver: WebDriver, products_url: [], type: str):
    products = []
    id = 1
    for product_url in products_url:
        if id % 30 == 0:
            driver = firefoxService.renew_session(driver)
        logger.debug(str(id) + ' -Getting products details for product url: ' + product_url)
        driver.implicitly_wait(5)
        driver.get(product_url)
        sleep(5)
        while True:
            page_content = get_page_source_until_selector(driver, '.colors-container > a', TIME_OUT_URL)
            soup = get_soup_by_content(page_content)
            title_collection = tag_text('head > title', soup).strip()
            if title_collection != '*':
                break

        if driver.find_element_by_css_selector('.button-menu') == None:
            driver.find_element_by_css_selector('.button-menu').click()
        all_colors_number = int(re.sub('[^0-9]', '', tag_text('.available-in', soup)))
        for color_number in range(1, all_colors_number + 1):
            id += 1
            page_content = get_page_source_until_selector(driver, 'head > title', TIME_OUT_URL)
            soup = get_soup_by_content(page_content)
            title_collection = tag_text('head > title', soup).strip()
            title = re.sub(r'in.*$', '', title_collection).title()
            color = re.sub(r'.*in|\|.*', '', title_collection).title()
            title += ' ' + color
            image = image_src('div.swatch', soup)
            product_labels = tags_text('div.col-lg-4 > p>span', soup)
            product_values = []
            for product_value in tags_text('div.col-lg-4 > p', soup):
                product_values.append(re.sub(r'.*:', '', product_value).strip().title())
            collection = re.sub(r'.*\||®', '', title_collection).strip().title()
            tags = ','.join(product_values)
            tags += ',' + collection
            details = htmlTemplateService.create_product_template(product_labels, product_values)
            products.append(Product(title + str(id), image, '', title, VENDOR_NAME, '', type, details, tags))
            driver.find_element_by_css_selector('.colors-container > a:nth-child(3)').click()
            sleep(2)

    return products


def get_products_details(base_url, type: str, product_urls_number: int = 9999, counter: int = 0,
                         product_url_file_path: str = ''):
    driver = firefoxService.renew_session()
    driver = firefoxService.renew_session(driver)
    if urlFileService.is_url_file_empty(product_url_file_path):
        product_urls = get_products_url(driver, base_url)
        product_urls = set(product_urls)
        product_urls = list(product_urls)
        urlFileService.write_url_list_to_file(product_url_file_path, product_urls)
    else:
        first_index = product_urls_number * counter
        last_index = first_index + product_urls_number
        product_urls = urlFileService.read_url_list_from_file(product_url_file_path)[first_index:last_index]

    driver = firefoxService.renew_session(driver)
    products_details = get_all_products_details(driver, product_urls[:product_urls_number], type)
    driver.quit()
    return products_details

