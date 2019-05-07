#!/usr/bin/python3

import csvService
import productToShopifyCsvTransformer
import shawScrapingService
import republicScrapingService
from config import initialise_configurations, logger, csv_template_dir, TEMPLATE_FILE_NAME, url_file_dir


def shaw_carpet_collecting(counter: int):
    products_details = shawScrapingService.get_products_details(shawScrapingService.CARPET_URL, 1000,
                                                                url_file_dir() + shawScrapingService.SHAW_CARPET_URL_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    products_details.clear()
    csvService.append_csv_array_to_file(
        csv_template_dir() + str(counter) + shawScrapingService.SHAW_CARPET_CSV_FILE_NAME,
        shopify_csv_array)


def republic_laminate_collecting():
    products_details = republicScrapingService.get_products_details(republicScrapingService.LAMINATED_URL, 'Laminated')
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    products_details.clear()
    csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
                              csv_template_dir() + republicScrapingService.REPUBLIC_LAMINATED_CSV_FILE_NAME)
    csvService.append_csv_array_to_file(csv_template_dir() + republicScrapingService.REPUBLIC_LAMINATED_CSV_FILE_NAME,
                                        shopify_csv_array)


def republic_vinyl_collecting():
    products_details = republicScrapingService.get_products_details(republicScrapingService.VINYL_1_URL, 'Vinyl')
    products_details.extend(republicScrapingService.get_products_details(republicScrapingService.VINYL_2_URL, 'Vinyl'))
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    products_details.clear()
    csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
                              csv_template_dir() + republicScrapingService.REPUBLIC_VINYL_CSV_FILE_NAME)
    csvService.append_csv_array_to_file(csv_template_dir() + republicScrapingService.REPUBLIC_VINYL_CSV_FILE_NAME,
                                        shopify_csv_array)


def main():
    initialise_configurations()
    logger.info('Start collecting data')

    for counter in range(0, 9):
        shaw_carpet_collecting(counter)

    logger.info('Finish')


main()
