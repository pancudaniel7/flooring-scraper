from selenium.webdriver.phantomjs import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver

from src.model.Product import Product
from src.service.common import HTMLTemplateService
from src.service.common.CollectorService import get_soup_by_content, all_href_urls, tag_text, \
    all_attributes_for_all_elements, inner_html_str, tags_text
from src.service.common.SeleniumCollectorService import get_page_source_until_selector

BASE_URL = 'http://www.regalhardwoods.com'
CATEGORIES_URL = BASE_URL + '/floors'
REGAL_CSV_FILE_NAME = 'regal-hardwood-template.csv'

TIME_OUT_PRODUCT_DELAY = 4
TIME_OUT_URL_DELAY = 5

VENDOR_NAME = 'Regal Flooring'


def get_product_category_urls(driver: WebDriver, url: str):
    driver.get(url)
    page_content = get_page_source_until_selector(driver, '.mask', TIME_OUT_URL_DELAY)
    soup = get_soup_by_content(page_content)
    return [BASE_URL + url for url in all_href_urls('.brand-items .mask', soup)]


def get_product_urls(driver: WebDriver, category_urls: []):
    products_urls = []
    for category_url in category_urls:
        driver.get(category_url)
        page_content = get_page_source_until_selector(driver, '.mask', TIME_OUT_URL_DELAY)
        soup = get_soup_by_content(page_content)
        products_urls.extend([BASE_URL + url for url in all_href_urls('.brand-items .mask', soup)])
    return products_urls


def get_all_products_details(driver: WebDriver, product_urls: []):
    products_details = []
    for product_url in product_urls:
        driver.get(product_url)
        page_content = get_page_source_until_selector(driver, '.mask', TIME_OUT_URL_DELAY)
        soup = get_soup_by_content(page_content)
        # TODO: Refactor image size, the size exeedes the 20 mb limit
        # first_image = all_attributes_for_all_elements('.floor-visual.box .bg-cover', 'style', soup)[0].replace(
        #     'background-image:url(', '').replace(');', '')
        # second_image = all_attributes_for_all_elements(
        #     '.box.floor-slideshow.slideshow.gallery-js-ready.autorotation-disabled .bg-cover', 'style', soup)[
        #     0].replace('background-image:url(', '').replace(');', '')

        product_title = tag_text('.slide .text-holder h1', soup)
        product_details = inner_html_str('.box .info-list', soup)
        product_details_fields = HTMLTemplateService.extract_product_details_from_html(product_details, '.name',
                                                                                       '.value')
        product_details = HTMLTemplateService.create_product_details_template(product_details_fields[0],
                                                                              product_details_fields[1]).replace('::',
                                                                                                                 ':')
        tags = ",".join(tags_text('.value', soup))
        products_details.append(Product('', '', product_title, VENDOR_NAME, '', '', product_details,
                                        tags))
    return products_details


def get_products_details():
    driver = webdriver.WebDriver()
    category_urls = get_product_category_urls(driver, CATEGORIES_URL)
    product_urls = get_product_urls(driver, category_urls)
    products_details = get_all_products_details(driver,
                                                product_urls)
    driver.quit()
    return products_details
