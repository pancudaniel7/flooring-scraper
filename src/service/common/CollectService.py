from bs4 import BeautifulSoup
from requests import Session


def get_page_soup(session: Session, url: str):
    page = session.get(url)
    soup = BeautifulSoup(page.content, features="lxml")
    return soup


def all_href_urls(selector: str, soup: BeautifulSoup):
    tags = soup.select(selector + ' a')
    return [a['href'] for a in tags]


def all_images_urls(selector: str, soup: BeautifulSoup):
    images = soup.select(selector + ' img')
    return [img['src'] for img in images]


def tag_text(selector: str, soup: BeautifulSoup):
    return soup.select(selector)[0].text


def tags_text(selector: str, soup: BeautifulSoup):
    return list(map(lambda x: str(x.text).replace('\n', '').strip(), soup.select(selector)))


def inner_html_str(selector: str, soup: BeautifulSoup):
    return str(soup.select(selector)[0]).replace('\n', '').replace('\r', '')