from bs4 import BeautifulSoup
from requests import Session

from src.model.ProductUrls import ProductUrls


def get_page_soup(session: Session, url: str):
    page = session.get(url)
    return BeautifulSoup(page.content, features="lxml")


def get_soup_by_content(page_content: str):
    return BeautifulSoup(page_content, features="lxml")


def all_attributes_for_all_elements(selector: str, attribute: str, soup: BeautifulSoup):
    elements = soup.select(selector)
    return [e[attribute] for e in elements]


def all_href_urls(selector: str, soup: BeautifulSoup):
    elements = soup.select(selector + ' a')
    return [a['href'] for a in elements]


def get_all_collection_product_url(href_selector: str, collection_selector: str, collection_attribute: str,
                                   soup: BeautifulSoup):
    product_urls = []
    elements = soup.select(href_selector + ' a')
    urls = [a['href'] for a in elements]
    elements = soup.select(collection_selector)
    collections = [e[collection_attribute] for e in elements]
    for url, collection in zip(urls, collections):
        product_urls.append(ProductUrls(collection, [url]))
    return product_urls


def all_images_urls(selector: str, soup: BeautifulSoup):
    images = soup.select(selector + ' img')
    return [img['src'] for img in images]


def tag_text(selector: str, soup: BeautifulSoup):
    return soup.select(selector)[0].text.strip()


def tags_text(selector: str, soup: BeautifulSoup):
    return list(map(lambda x: str(x.text).replace('\n', '').strip(), soup.select(selector)))


def inner_html_str(selector: str, soup: BeautifulSoup):
    return str(soup.select(selector)[0]).replace('\r', '').replace('\n', '')
