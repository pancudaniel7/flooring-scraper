from selenium.webdriver.phantomjs import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver

from src.model.Product import Product
from src.service.common import HTMLTemplateService
from src.service.common.CollectorService import get_soup_by_content, tag_text, \
    all_attributes_for_all_elements, inner_html_str, tags_text, get_all_collection_product_url
from src.service.common.SeleniumCollectorService import get_page_source_until_selector

BASE_URL = 'https://knoasflooring.com/product-category'
LAMINATE_URL = BASE_URL + '/laminate-floors'
VINYL_URL = BASE_URL + '/vinyl-floors'
WOOD_URL = BASE_URL + '/wood-floors'
ACCESSORIES_URL = BASE_URL + '/accessories'
KNOAS_CSV_FILE_NAME = 'knoas-hardwood-template.csv'

TIME_OUT_PRODUCT_DELAY = 4
TIME_OUT_URL_DELAY = 5

VENDOR_NAME = 'Knoas Flooring'


def get_product_category_urls(driver: WebDriver, url: str):
    driver.get(url)
    page_content = get_page_source_until_selector(driver, '.entry-title', TIME_OUT_URL_DELAY)
    soup = get_soup_by_content(page_content)
    return [product_url for product_url in
            get_all_collection_product_url('.woocom-list-content .entry-title', '.woocom-list-content .entry-title a',
                                           'title', soup)]


def get_all_products_details(driver: WebDriver, product_urls: []):
    products_details = []
    id = 1
    for product_url in product_urls:
        driver.get(product_url)
        page_content = get_page_source_until_selector(driver, '.mask', TIME_OUT_URL_DELAY)
        soup = get_soup_by_content(page_content)

        first_image = all_attributes_for_all_elements('.floor-visual.box .bg-cover', 'style', soup)[0].replace(
            'background-image:url(', '').replace(');', '')
        second_image = all_attributes_for_all_elements(
            '.box.floor-slideshow.slideshow.gallery-js-ready.autorotation-disabled .bg-cover', 'style', soup)[
            0].replace('background-image:url(', '').replace(');', '')

        product_title = tag_text('.slide .text-holder h1', soup)
        product_details = inner_html_str('.box .info-list', soup)
        product_details_fields = HTMLTemplateService.extract_product_details_from_html(product_details, '.name',
                                                                                       '.value')
        product_details = HTMLTemplateService.create_product_details_template(product_details_fields[0],
                                                                              product_details_fields[1]).replace('::',
                                                                                                                 ':')
        tags = ",".join(tags_text('.value', soup))
        products_details.append(
            Product(product_title + str(id), '', '', product_title, VENDOR_NAME, '', '', product_details,
                    tags))
        id += 1
    return products_details


def get_products_details():
    driver = webdriver.WebDriver()
    # TODO: Continue to get product details
    product_collection_urls = get_product_category_urls(driver, LAMINATE_URL)
    driver.quit()
    return None
