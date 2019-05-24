from bs4 import BeautifulSoup
from config import logger
from requests import Session
from selenium.webdriver.firefox.webdriver import WebDriver

from service.collector.seleniumCollectorService import get_page_source_after_click_with_delay, \
    get_page_source_until_selector_with_delay
from service.session import firefoxService


def get_page_soup(session: Session, url: str):
    page = session.get(url)
    return BeautifulSoup(page.content, features="lxml")


def get_soup_by_content(page_content: str):
    return BeautifulSoup(page_content, features="lxml")


def attribute_value_for_all_elements(selector: str, attribute: str, soup: BeautifulSoup):
    elements = soup.select(selector)
    return [e.get(attribute) for e in elements if e.get(attribute, '') != '']


def attribute_value_element(selector: str, attribute: str, soup: BeautifulSoup):
    elements = soup.select(selector)
    img_urls = [e.get(attribute) for e in elements if e.get(attribute, '') != '']
    return img_urls[0] if len(img_urls) > 0 else ''


def href_url_index_0(selector: str, soup: BeautifulSoup):
    elements = soup.select(selector + ' a')
    return [a['href'] for a in elements][0]


def all_href_urls(selector: str, soup: BeautifulSoup):
    elements = soup.select(selector + ' a')
    return [a['href'] for a in elements if a.get('href', '') != '']


def all_images_src(selector: str, soup: BeautifulSoup):
    images = soup.select(selector + ' img')
    return [img['src'] for img in images]


def image_src(selector: str, soup: BeautifulSoup):
    img = soup.select(selector + ' img')[0]
    return img['src'] if img.get('src', '') != '' else ''


def tag_text(selector: str, soup: BeautifulSoup):
    return soup.select(selector)[0].text.replace('\r', '').replace('\n', '').strip() if len(
        soup.select(selector)) > 0 else ''


def tags_text(selector: str, soup: BeautifulSoup):
    return list(map(lambda x: str(x.text).replace('\r', '').replace('\n', '').strip(), soup.select(selector)))


def inner_html(selector: str, soup: BeautifulSoup):
    return soup.select(selector)


def inner_html_str(selector: str, soup: BeautifulSoup):
    return [str(html).replace('\r', '').replace('\n', '') for html in soup.select(selector)]


def inner_html_str_index_0(selector: str, soup: BeautifulSoup):
    return str(soup.select(selector)[0]).replace('\r', '').replace('\n', '') if len(soup.select(selector)) > 0 else ''


def inner_html_str_at_index(selector: str, index: int, soup: BeautifulSoup):
    return str(soup.select(selector)[index]).replace('\r', '').replace('\n', '')


def extract_product_details_from_html(content_html: str, labels_selector: str, values_selector: str):
    soup = get_soup_by_content(content_html)
    labels = tags_text(labels_selector, soup)
    values = tags_text(values_selector, soup)
    return [labels, values]


def get_product_urls_for_pages(driver: WebDriver, pages_urls: [], urls_selector: str, selector_timeout, delay):
    urls = []
    id = 1
    logger.debug('Pages urls size: {} '.format(len(pages_urls)))
    for page_number in range(0, len(pages_urls)):
        if id % 50 == 0:
            driver = firefoxService.renew_session(driver)
        logger.debug('Getting selected urls for page number {}:{} '.format(page_number, pages_urls[page_number]))
        driver.get(pages_urls[page_number])
        page_content = get_page_source_until_selector_with_delay(driver,
                                                                 'img',
                                                                 selector_timeout,
                                                                 delay)
        soup = get_soup_by_content(page_content)
        urls.extend(attribute_value_for_all_elements(urls_selector, 'href', soup))
        id += 1
    return list(set(urls))
