import requests
from requests import Session

from src.Config import logger
from src.model.Product import Product
from src.service.CollectCommonService import get_all_href_urls, get_page_soup, get_all_images_urls

PRODUCTS_URL = 'http://johnsonhardwood.com/products/'
VENDOR_NAME = 'Johnson Hardwood'


def get_all_categories_products_urls(session: Session):
    category_urls = get_all_href_urls('#filter-container .serieses', get_page_soup(session, PRODUCTS_URL))
    logger.debug('Finish getting category urls from: ' + PRODUCTS_URL)

    products_urls = []
    for category_url in category_urls:
        products_urls.extend(get_all_href_urls('#filter-container .products', get_page_soup(session, category_url)))
    return products_urls


def get_product_details(session: Session, product_url: str):
    soup = get_page_soup(session, product_url)
    get_all_images_urls('#product-gallery .item.active .image-wrapper', soup)[0]
    ",".join(get_all_images_urls('#product-gallery .item .image-wrapper', soup))


def get_products_details():
    session = requests.session()

    get_product_details(session, 'http://johnsonhardwood.com/products/ame-ahm19001-maibock/')
    session.close()
