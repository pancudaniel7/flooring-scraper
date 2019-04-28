# TODO: Finish this one at the end
from selenium.webdriver.phantomjs import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver

from Product import Product
import htmlTemplateService
from collectorService import get_soup_by_content, all_href_urls, tag_text, \
    all_attributes_for_all_elements, inner_html_str_index_0, tags_text
from seleniumCollectorService import get_page_source_until_selector

BASE_URL = 'http://lawsonfloors.com/portfolio_category'
ENGINEERED_WOOD_FLOORING_CATEGORY_URL = BASE_URL + '/engineered-wood-flooring'
LAMINATE_FLOORING_CATEGORY_URL = BASE_URL + '/laminate-flooring-collections'
WATERPROOF_CATEGORY_URL = BASE_URL + '/waterproof-flooring'

LAWSON_CSV_FILE_NAME = 'lawson-hardwood-template.csv'

TIME_OUT_PRODUCT = 4
TIME_OUT_URL = 5

VENDOR_NAME = 'Lawson Flooring'


def get_product_category_urls(driver: WebDriver, url: str):
    driver.get(url)
    page_content = get_page_source_until_selector(driver, '.image-wrap', TIME_OUT_URL)
    soup = get_soup_by_content(page_content)
    return [BASE_URL + url for url in all_href_urls('.content #content', soup)]


def get_all_products_details(driver: WebDriver, category_urls: []):
    products_details = []
    id = 1
    for category_url in category_urls:
        driver.get(category_url)
        page_content = get_page_source_until_selector(driver, '.mask', TIME_OUT_URL)
        soup = get_soup_by_content(page_content)
        first_image = all_attributes_for_all_elements('.floor-visual.box .bg-cover', 'style', soup)[0].replace(
            'background-image:url(', '').replace(');', '')
        second_image = all_attributes_for_all_elements(
            '.box.floor-slideshow.slideshow.gallery-js-ready.autorotation-disabled .bg-cover', 'style', soup)[
            0].replace('background-image:url(', '').replace(');', '')

        product_title = tag_text('.slide .text-holder h1', soup)
        product_details = inner_html_str_index_0('.box .info-list', soup)
        product_details_fields = htmlTemplateService.extract_product_details_from_html(product_details, '.name',
                                                                                       '.value')
        product_details = htmlTemplateService.create_product_template(product_details_fields[0],
                                                                      product_details_fields[1]).replace('::',
                                                                                                         ':')
        tags = ",".join(tags_text('.value', soup))
        products_details.append(
            Product(product_title + str(id), first_image, second_image, product_title, VENDOR_NAME, '', '',
                    product_details,
                    tags))
        id += 1
    return products_details


def get_products_details():
    driver = webdriver.WebDriver()
    category_urls = get_product_category_urls(driver, ENGINEERED_WOOD_FLOORING_CATEGORY_URL)
    category_urls.extend(get_product_category_urls(driver, LAMINATE_FLOORING_CATEGORY_URL))
    category_urls.extend(get_product_category_urls(driver, WATERPROOF_CATEGORY_URL))
    driver.quit()
    return None
