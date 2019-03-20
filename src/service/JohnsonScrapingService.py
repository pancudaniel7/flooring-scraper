import requests
from bs4 import BeautifulSoup
from requests import Session

from src.Config import logger


def get_page_soup(session: Session, url: str):
    page = session.get(url)
    soup = BeautifulSoup(page.content, features="lxml")
    return soup


def get_all_href_urls(selector: str, soup: BeautifulSoup):
    tags = soup.select(selector + ' a')
    for a in tags:
        yield (a['href'])


PRODUCTS_URL = 'http://johnsonhardwood.com/products/'


def get_all_products_urls():
    with requests.Session() as session:
        products_urls = None
        try:
            category_urls = list(
                get_all_href_urls('#filter-container .serieses', get_page_soup(session, PRODUCTS_URL)))
            logger.debug('Finish getting category urls from: ' + PRODUCTS_URL)

            products_urls = []
            for category_url in category_urls:
                products_urls.extend(
                    list(get_all_href_urls('#filter-container .products', get_page_soup(session, category_url))))
        except Exception as e:
            logger.error('Error: ' + e)
        return products_urls