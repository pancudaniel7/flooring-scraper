from bs4 import BeautifulSoup
from requests import Session


def get_page_soup(session: Session, url: str):
    page = session.get(url)
    soup = BeautifulSoup(page.content, features="lxml")
    return soup


def get_all_href_urls(selector: str, soup: BeautifulSoup):
    tags = soup.select(selector + ' a')
    href_urls = []
    for a in tags:
        href_urls.append(a['href'])
    return href_urls

def get_all_images_urls(selector: str, soup: BeautifulSoup):
    images = soup.select(selector + ' img')
    image_urls = []
    for img in images:
        image_urls.append(img['src'])
    return image_urls


def get_h1_text(selector: str, soup: BeautifulSoup):
    return soup.select(selector + ' h1')


def get_spans_text(selector: str, soup: BeautifulSoup):
    return soup.select(selector + ' span')
