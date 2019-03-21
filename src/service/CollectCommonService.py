from bs4 import BeautifulSoup
from requests import Session


def get_page_soup(session: Session, url: str):
    page = session.get(url)
    soup = BeautifulSoup(page.content, features="lxml")
    return soup


def get_all_href_urls(selector: str, soup: BeautifulSoup):
    tags = soup.select(selector + ' a')
    for a in tags:
        yield (a['href'])


def get_all_images_urls(selector: str, soup: BeautifulSoup):
    images = soup.select(selector + ' img')
    for img in images:
        yield (img['src'])


def get_h1_text(selector: str, soup: BeautifulSoup):
    return soup.select(selector + ' h1')


def get_span_text(selector: str, soup: BeautifulSoup):
    return soup.select(selector + ' span')


def get_spans_text(selector: str, soup: BeautifulSoup):
    return soup.select(selector + ' h1')