import requests
from requests import Session

from src.Config import logger
from src.model.Product import Product
from src.service.CollectCommonService import get_all_href_urls, get_page_soup, get_all_images_urls, get_tag_text, \
    get_inner_html_str, get_tags_text

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
    variant_images = get_all_images_urls('#product-gallery .item .image-wrapper', soup)[1]
    title = get_tag_text('.main .container .header-wrapper h1', soup)
    product_code = get_tag_text('.main .container .header-wrapper h1 + span', soup)
    product_details = get_inner_html_str('.main .entry-content.container .details', soup)
    tags = ", ".join(get_tags_text('.main .entry-content.container .details span', soup))

    return Product(image, variant_images,
                   title, JOHNSOON_VENDOR_NAME,
                   product_code, '',
                   product_details, tags)


def get_products_details():
    session = requests.session()
    products_urls = get_all_categories_products_urls(session, PRODUCTS_URL)
    products_details = [get_product_details(session, url) for url in products_urls]
    session.close()
    return products_details
