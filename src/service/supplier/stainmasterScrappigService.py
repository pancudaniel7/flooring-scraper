import re
from selenium.webdriver.firefox.webdriver import WebDriver
from config import logger
from model.Product import Product
from service.collector.collectorService import get_soup_by_content, tag_text, all_href_urls, tags_text, image_src, \
    inner_html
from service.session import firefoxService
from service.collector.seleniumCollectorService import get_page_source_until_selector, \
    get_page_source_until_selector_with_delay, get_page_source_after_click_with_delay
from service.html import htmlTemplateService
from time import sleep
from service.url import urlFileService

BASE_URL = 'https://www.stainmaster.com'
CARPET_URL = BASE_URL + '/carpet/products/allcarpets/'
VINYL_1_URL = BASE_URL + '/vinyl/products/allvinyls/'
STAINMASTER_CARPET_CSV_FILE_NAME = 'stainmaster-carpet-template.csv'
STAINMASTER_VINYL_CSV_FILE_NAME = 'stainmaster-vinyl-template.csv'
STAINMASTER_VINYL_URL_FILE_NAME = 'stainmaster_vinyl-url.txt'
STAINMASTER_CARPET_URL_FILE_NAME = 'stainmaster-carpet-url.txt'
VENDOR_NAME = 'StainMaster'

TIME_OUT_PRODUCT = 10
TIME_OUT_URL = 4000
TIME_DELAY = 4


def get_products_url(driver: WebDriver, url: str):
    products_url = set()
    logger.debug('Getting pages number from: ' + url)
    driver.get(url)
    page_content = get_page_source_until_selector_with_delay(driver, '.pagination > li:nth-child(5)', TIME_OUT_URL, TIME_OUT_PRODUCT)
    driver.find_element_by_css_selector('.pagination > li:nth-child(5) > a').click()
    page_content = get_page_source_until_selector_with_delay(driver, '.pagination > li:nth-child(5) > a', TIME_OUT_URL,
                                                             TIME_OUT_PRODUCT)
    soup = get_soup_by_content(page_content)

    number_of_pages = int(tag_text('.pagination > li:nth-child(5)>a', soup).strip())
    for page_number in range(1, number_of_pages + 1):
        new_url = url + '?pageNumber=' + str(page_number) + '&productSelect=20&Favorites=false'
        logger.debug(str(page_number) + '- Getting product url for: ' + url)
        driver.get(new_url)
        page_content = get_page_source_until_selector(driver,
                                                      'div.col-xs-6 > div:nth-child(1) > div:nth-child(2) > a:nth-child(3)',
                                                      TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        for product in all_href_urls('div.row:nth-child(5)', soup):
            set.add(products_url, BASE_URL + product.strip())

    return list(products_url)


def get_all_products_details(driver: WebDriver, products_url: [], type: str):
    products = []
    id = 1
    for product_url in products_url:
        if id % 30 == 0:
            driver = firefoxService.renew_session(driver)
        logger.debug(str(id) + ' -Getting products details for product url: ' + product_url)
        driver.get(product_url)
        while True:
            if type != 'Carpet':
                page_content = get_page_source_until_selector_with_delay(driver, 'head > title', TIME_OUT_URL, TIME_DELAY)
            else:
                page_content = get_page_source_until_selector_with_delay(driver, '.colors-container > a', TIME_OUT_URL,
                                                                         TIME_DELAY)
            soup = get_soup_by_content(page_content)
            title_collection = tag_text('head > title', soup).strip()
            if title_collection != '*':
                break
            sleep(TIME_DELAY)
        if type == 'Carpet' and driver.find_element_by_css_selector('.button-menu') is not None:
            if tag_text('#moreColorsButton > span:nth-child(2)', soup) != '+0 Colors':
                driver.find_element_by_css_selector('.button-menu').click()
            all_colors_number = int(re.sub('[^0-9]', '', tag_text('.available-in', soup)))
        else:
            all_colors_number = 1

        for color_number in range(1, all_colors_number + 1):
            if type == 'Carpet':
                color_selector = '.colors-container > a:nth-child(3)'
                if soup.find('div',{'class':'hidden'}) is not None:
                    color_selector = '.colors-container > a'
                page_content = get_page_source_after_click_with_delay(driver, color_selector,
                                                                      TIME_OUT_URL, TIME_DELAY)
            else:
                page_content = get_page_source_until_selector(driver, 'head > title', TIME_OUT_URL)
            soup = get_soup_by_content(page_content)
            title_collection = tag_text('head > title', soup).strip()
            title = re.sub(r'in.*$', '', title_collection).title().strip()
            if type == 'Carpet':
                color = re.sub(r'.*in |\|.*', '', title_collection).title().strip()
                title += ' ' + color
                collection = re.sub(r'.*\||®', '', title_collection).strip().title()
                image = re.sub(r'\?.*', '', image_src('div.swatch', soup))
            else:
                collection = re.sub(r'.*in ', '', title_collection).strip().title()
                image = BASE_URL + re.sub(r'\?.*', '', image_src('div.swatch', soup))
            product_labels = [re.sub(r':', '', product_label) for product_label in
                              tags_text('.items > div > p > strong', soup)]
            product_values = []
            for product_value in tags_text('.items > div > p', soup):
                product_values.append(re.sub(r'.*:|®', '', product_value).strip().title())
            tags = ','.join(product_values)
            tags += ',' + collection
            details = htmlTemplateService.create_product_template(product_labels, product_values)
            products.append(Product(title + str(id), image, '', title, VENDOR_NAME, '', type, details, tags))
        id += 1
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
