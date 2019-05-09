#!/usr/bin/python3

from config import url_file_dir, csv_template_dir, initialise_configurations, logger
from service.csv import csvService
from service.supplier import shawScrapingService
from transformer import productToShopifyCsvTransformer


def shaw_carpet_collecting(counter: int):
    products_details = shawScrapingService.get_products_details(shawScrapingService.CARPET_URL, 1000, counter,
                                                                url_file_dir() + shawScrapingService.SHAW_CARPET_URL_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    products_details.clear()
    csvService.append_csv_array_to_file(csv_template_dir() + shawScrapingService.SHAW_CARPET_CSV_FILE_NAME,
                                        shopify_csv_array)


def main():
    initialise_configurations()
    logger.info('Start collecting data')

    for counter in range(0, 9):
        shaw_carpet_collecting(counter)

    logger.info('Finish')


main()
