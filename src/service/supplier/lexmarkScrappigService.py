import re
from selenium.webdriver.firefox.webdriver import WebDriver
from config import logger
from model.Product import Product
from service.collector.collectorService import get_soup_by_content, tag_text, all_href_urls, tags_text, image_src, \
    inner_html, href_url_index_0
from service.session import firefoxService
from service.collector.seleniumCollectorService import get_page_source_until_selector, get_page_source_after_click
from service.html import htmlTemplateService
from time import sleep
from service.url import urlFileService

BASE_URL = 'https://www.lexmarkcarpet.com'
CARPET_URL = BASE_URL + '/residential/products/'
LEXMARK_CARPET_CSV_FILE_NAME = 'lexmark-carpet-template.csv'
LEXMARK_CARPET_URL_FILE_NAME = 'lexmark-carpet-url.txt'
VENDOR_NAME = 'Lexmark'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 1500
TIME_DELAY = 1


def get_products_url(driver: WebDriver, url: str):
    products_url = set()
    id = 0
    while True:
        id += 1
        url = CARPET_URL + 'page/' + str(id) + '/'
        logger.debug(str(id) + '-Getting pages number from: ' + url)
        driver.get(url)
        page_content = get_page_source_until_selector(driver,
                                                      '.product-lists > div > div > div:nth-child(2) > a:nth-child(1) > img',
                                                      TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        for product_url in all_href_urls('.product-lists--items>div:nth-child(2)', soup):
            set.add(products_url, product_url)
        if len(soup.select('div.right>a')) == 0:
            break
    return list(products_url)


def get_all_products_details(driver: WebDriver, products_url: [], type: str):
    products = []
    id = 1
    for product_url in products_url:
        if id % 30 == 0:
            driver = firefoxService.renew_session(driver)
        logger.debug(str(id) + ' -Getting products details for product url: ' + product_url)
        driver.get(product_url)
        page_content = get_page_source_until_selector(driver, '.img-responsive', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        title = tag_text('.violet-text', soup).strip().title()
        all_colors_number = len(all_href_urls('#content1 > ul:nth-child(1) > li', soup))
        collection = ''
        product_labels = [re.sub(r':', '', product_label.strip().title()) for product_label in
                          tags_text('div > p > strong', soup)]
        product_values = []
        for product_value in tags_text('.product-specs>div>p', soup):
            product_values.append(re.sub(r'.*\t', '', product_value).strip().title())
        for product_value in tags_text('.col-md-4 > div:nth-child(1) > div > p', soup):
            product_values.append(re.sub(r'.*\t', '', product_value).strip().title())
        tags = ','.join(product_values)
        tags += ',' + collection
        details = htmlTemplateService.create_product_template(product_labels, product_values)

        for color_number in range(1, all_colors_number + 1):
            color = tag_text('#content1 > ul:nth-child(1) > li:nth-child(' + str(color_number) + ') > span:nth-child(2)', soup)
            title_color = title + ' ' + color
            image = all_href_urls('#content1 > ul:nth-child(1) > li:nth-child(' + str(color_number) + ')', soup)[0]
            products.append(
                Product(title_color, image, '', title_color, VENDOR_NAME, '', type, details, tags))
        id += 1
    return products


def get_products_details(base_url, type: str, product_urls_number: int = 9999, counter: int = 0,
                         product_url_file_path: str = ''):
    driver = firefoxService.renew_session()
    driver = firefoxService.renew_session(driver)
    if urlFileService.is_url_file_empty(product_url_file_path):
        product_urls = get_products_url(driver, base_url)
        urlFileService.write_url_list_to_file(product_url_file_path, product_urls)
    else:
        first_index = product_urls_number * counter
        last_index = first_index + product_urls_number
        product_urls = urlFileService.read_url_list_from_file(product_url_file_path)[first_index:last_index]

    driver = firefoxService.renew_session(driver)
    products_details = get_all_products_details(driver, product_urls[:product_urls_number], type)
    driver.quit()
    return products_details
