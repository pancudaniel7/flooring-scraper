#!/usr/bin/python3
from config import csv_template_dir, TEMPLATE_FILE_NAME
from service.csv import csvService
from service.supplier import bruceScrapingService
from transformer import productToShopifyCsvTransformer


def bruce_carpet_collecting():
    products_details = bruceScrapingService.get_products_details()
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
                              csv_template_dir() + bruceScrapingService.BRUCE_CSV_FILE_NAME)
    csvService.append_csv_array_to_file(csv_template_dir() + bruceScrapingService.BRUCE_CSV_FILE_NAME,
                                        shopify_csv_array)
