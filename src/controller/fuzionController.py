import config
from service.csv import csvService
from service.supplier import tarkettScrapingService, fuzionScrapingService
from transformer import productToShopifyCsvTransformer


def collecting():

    product_details = fuzionScrapingService.get_product_details()
    csvService.clean_csv_file(config.csv_template_dir() + config.TEMPLATE_FILE_NAME,
                              config.csv_template_dir() + fuzionScrapingService.FUZION_CSV_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in product_details]
    product_details.clear()
    csvService.append_csv_array_to_file(
        config.csv_template_dir() + fuzionScrapingService.FUZION_CSV_FILE_NAME,
        shopify_csv_array)
