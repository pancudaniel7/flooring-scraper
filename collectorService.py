from bs4 import BeautifulSoup
from requests import Session


def get_page_soup(session: Session, url: str):
    page = session.get(url)
    return BeautifulSoup(page.content, features="lxml")


def get_soup_by_content(page_content: str):
    return BeautifulSoup(page_content, features="lxml")


def all_attributes_for_all_elements(selector: str, attribute: str, soup: BeautifulSoup):
    elements = soup.select(selector)
    return [e.get(attribute) for e in elements if e.get(attribute, '') != '']


def href_url_index_0(selector: str, soup: BeautifulSoup):
    elements = soup.select(selector + ' a')
    return [a['href'] for a in elements][0]


def all_href_urls(selector: str, soup: BeautifulSoup):
    elements = soup.select(selector + ' a')
    return [a['href'] for a in elements]


def all_images_src(selector: str, soup: BeautifulSoup):
    images = soup.select(selector + ' img')
    return [img['src'] for img in images]


def tag_text(selector: str, soup: BeautifulSoup):
    return soup.select(selector)[0].text.strip()


def tags_text(selector: str, soup: BeautifulSoup):
    return list(map(lambda x: str(x.text).replace('\n', '').strip(), soup.select(selector)))


def inner_html(selector: str, soup: BeautifulSoup):
    return soup.select(selector)


def inner_html_str_index_0(selector: str, soup: BeautifulSoup):
    return str(soup.select(selector)[0]).replace('\r', '').replace('\n', '')


def inner_html_str_at_index(selector: str, index: int, soup: BeautifulSoup):
    return str(soup.select(selector)[index]).replace('\r', '').replace('\n', '')
