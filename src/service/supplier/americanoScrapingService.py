from selenium.webdriver.firefox.webdriver import WebDriver

from config import logger
from model.Product import Product
from service.collector import collectorService
from service.collector.collectorService import get_soup_by_content, tag_text, tags_text, \
    images_src
from service.collector.seleniumCollectorService import get_page_source_until_selector_with_delay
from service.session import firefoxService
from selenium.webdriver.firefox.webdriver import WebDriver

from config import logger
from model.Product import Product
from service.collector import collectorService
from service.collector.collectorService import get_soup_by_content, tag_text, tags_text, \
    images_src
from service.collector.seleniumCollectorService import get_page_source_until_selector_with_delay
from service.session import firefoxService

BASE_URL = 'https://americanolean.com'
COLLECTION_URL = BASE_URL + '/browse_product_series.cfm'
AMERICANO_CSV_FILE_NAME = 'americano-template.csv'

TIME_OUT = 120
SLEEP_DELAY = 1

TIME_OUT_CLICK = 120
SLEEP_CLICK_DELAY = 1

VENDOR_NAME = 'Americanolean'


def get_products_details_from_collections(driver: WebDriver, product_urls: []):
    products_details = []
    id = 1
    logger.debug('Collection size: {} '.format(len(product_urls)))
    for url in product_urls:
        logger.debug('Collecting product details for url {}:{} '.format(id, url))
        if id % 10 == 0:
            driver = firefoxService.renew_session(driver)
        driver.get(url)
        page_content = get_page_source_until_selector_with_delay(driver, 'img', TIME_OUT, SLEEP_DELAY)
        soup = get_soup_by_content(page_content)

        collection = tag_text(
            '#pgTitleSec > div.seriesTitleCrumContainer > h1',
            soup).title().replace('™', '')
        products_data = collectorService.inner_html_str_index_0('#submenu_4 .submenuContent table',
                                                                soup)
        tags = collection
        titles = tags_text('#seriesRoomsceneLarge div.details > div.seriesItemName > p:nth-child(2) > b', soup)
        product_types = tags_text('#seriesRoomsceneLarge div.details > div.seriesItemName > p:nth-child(3)', soup)
        images = images_src(
            '#seriesRoomsceneLarge div.photos > ',
            soup)
        images = [BASE_URL + img for img in images]
        for title, image, product_type in zip(titles, images, product_types):
            products_details.append(
                Product(title + str(id), image, '', title,
                        VENDOR_NAME, '',
                        product_type, products_data,
                        tags))
        id += 1

    return products_details


def get_products_details():
    driver = firefoxService.renew_session()
    collection_urls = collectorService.get_product_urls_for_pages(driver,
                                                                  [COLLECTION_URL],
                                                                  '#pgMainContent > ul > li > ul > li > a',
                                                                  TIME_OUT, 0)
    collection_urls = list(set(BASE_URL + url if '/' in url else BASE_URL + '/' + url for url in collection_urls))
    driver = firefoxService.renew_session(driver)
    products_details = list(set(get_products_details_from_collections(driver,
                                                                      collection_urls)))
    driver.quit()
    return products_details
