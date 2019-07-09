import config
from config import url_file_dir, csv_template_dir, initialise_configurations
from service.csv import csvService
from service.supplier import shawScrapingService
from transformer import productToShopifyCsvTransformer


def carpet_collecting(counter: int):
    products_details = shawScrapingService.get_products_details_with_counter(shawScrapingService.CARPET_URL, 1000,
                                                                             counter,
                                                                             url_file_dir() + shawScrapingService.SHAW_CARPET_URL_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    products_details.clear()
    csvService.append_csv_array_to_file(csv_template_dir() + shawScrapingService.SHAW_CARPET_CSV_FILE_NAME,
                                        shopify_csv_array)


def collecting(type_url: str, csv_file_name: str):
    products_details = shawScrapingService.get_products_details(type_url)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    products_details.clear()
    csvService.clean_csv_file(config.csv_template_dir() + config.TEMPLATE_FILE_NAME,
                              config.csv_template_dir() + csv_file_name)
    csvService.append_csv_array_to_file(csv_template_dir() + csv_file_name,
                                        shopify_csv_array)
