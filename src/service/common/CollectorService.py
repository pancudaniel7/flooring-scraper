from bs4 import BeautifulSoup
from requests import Session


def get_page_soup(session: Session, url: str):
    page = session.get(url)
    return BeautifulSoup(page.content, features="lxml")


def get_soup_by_page_content(page: str):
    return BeautifulSoup(page, features="lxml")


def all_attributes_for_all_elements(selector: str, attribute: str, soup: BeautifulSoup):
    elements = soup.select(selector)
    return [e[attribute] for e in elements]


def all_href_urls(selector: str, soup: BeautifulSoup):
    elements = soup.select(selector + ' a')
    return [a['href'] for a in elements]


def all_images_urls(selector: str, soup: BeautifulSoup):
    images = soup.select(selector + ' img')
    return [img['src'] for img in images]


def tag_text(selector: str, soup: BeautifulSoup):
    return soup.select(selector)[0].text.strip()


def tags_text(selector: str, soup: BeautifulSoup):
    return list(map(lambda x: str(x.text).replace('\n', '').strip(), soup.select(selector)))


def inner_html_str(selector: str, soup: BeautifulSoup):
    return str(soup.select(selector)[0]).replace('\n', '').replace('\r', '')
