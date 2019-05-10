#!/usr/bin/python3

from config import url_file_dir, csv_template_dir, initialise_configurations, logger
from service.csv import csvService
from service.supplier import tarkettScrapingService
from transformer import productToShopifyCsvTransformer


def tarkett_laminate_collecting():
    product_details = tarkettScrapingService.get_products_details(tarkettScrapingService.LAMINATED_URL, ["Laminated"])


def main():
    initialise_configurations()
    logger.info('Start collecting data')

    tarkett_laminate_collecting()

    logger.info('Finish')


main()
