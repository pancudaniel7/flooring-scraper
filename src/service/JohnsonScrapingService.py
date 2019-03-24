import requests
from requests import Session

from src.Config import logger
from src.model.Product import Product
from src.service.CollectCommonService import get_all_href_urls, get_page_soup, get_all_images_urls, get_tag_text, \
    get_inner_html

PRODUCTS_URL = 'http://johnsonhardwood.com/products/'
JOHNSOON_VENDOR_NAME = 'Johnson Hardwood'
JOHNSOON_CSV_FILE_NAME = 'johnson-hardwood-template.csv'


def get_all_categories_products_urls(session: Session, url: str):
    category_urls = get_all_href_urls('#filter-container .serieses', get_page_soup(session, url))
    logger.debug('Finish getting category urls from: ' + PRODUCTS_URL)

    products_urls = []
    for category_url in category_urls:
        products_urls.extend(get_all_href_urls('#filter-container .products', get_page_soup(session, category_url)))
    return products_urls


def get_product_details(session: Session, product_url: str):
    soup = get_page_soup(session, product_url)
    image = get_all_images_urls('#product-gallery .item.active .image-wrapper', soup)[0]
    # TODO: Fix variant images to get all
    variant_images = get_all_images_urls('#product-gallery .item .image-wrapper', soup)[0]
    title = get_tag_text('.main .container .header-wrapper h1', soup)
    product_code = get_tag_text('.main .container .header-wrapper h1 + span', soup)
    product_details = get_inner_html('.main .entry-content.container .details', soup)
    return Product(image, variant_images,
                   title, JOHNSOON_VENDOR_NAME,
                   product_code, '',
                   product_details, '')


def get_products_details():
    session = requests.session()
    products_urls = get_all_categories_products_urls(session, PRODUCTS_URL)
    products_details = []
    for url in products_urls:
        products_details.append(get_product_details(session, url))
    session.close()
    return products_details
