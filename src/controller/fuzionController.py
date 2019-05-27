import config
from config import url_file_dir, csv_template_dir, initialise_configurations
from service.csv import csvService
from service.supplier import shawScrapingService, fuzionScrapingService
from transformer import productToShopifyCsvTransformer


def collecting():
    products_details = fuzionScrapingService.get_product_details()
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    products_details.clear()
    csvService.clean_csv_file(config.csv_template_dir() + config.TEMPLATE_FILE_NAME,
                              config.csv_template_dir() + fuzionScrapingService.FUZION_CSV_FILE_NAME)
    csvService.append_csv_array_to_file(csv_template_dir() + fuzionScrapingService.FUZION_CSV_FILE_NAME,
                                        shopify_csv_array)
