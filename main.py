#!/usr/bin/python3

import os

import csvService
import productToShopifyCsvTransformer
import shawScrapingService
from config import initialise_configurations, logger, csv_template_dir, TEMPLATE_FILE_NAME, url_file_dir


def shaw_carpet_collecting():
    products_details = shawScrapingService.get_products_details(shawScrapingService.CARPET_URL, 1000,
                                                                url_file_dir() + shawScrapingService.SHAW_CARPET_URL_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    products_details.clear()
    csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
                              csv_template_dir() + shawScrapingService.SHAW_CARPET_CSV_FILE_NAME)
    csvService.append_csv_array_to_file(csv_template_dir() + shawScrapingService.SHAW_CARPET_CSV_FILE_NAME,
                                        shopify_csv_array)


def main():
    initialise_configurations()
    logger.info('Start collecting data')

    shaw_carpet_collecting()

    logger.info('Finish')
    os.system('poweroff')


main()
