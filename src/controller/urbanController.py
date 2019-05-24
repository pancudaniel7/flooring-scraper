import config
from service.csv import csvService
from service.supplier import urbanScrapingService
from transformer import productToShopifyCsvTransformer


def collecting():
    product_details = urbanScrapingService.get_products_details()
    csvService.clean_csv_file(config.csv_template_dir() + config.TEMPLATE_FILE_NAME,
                              config.csv_template_dir() + urbanScrapingService.URBAN_CSV_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in product_details]
    product_details.clear()
    csvService.append_csv_array_to_file(
        config.csv_template_dir() + urbanScrapingService.URBAN_CSV_FILE_NAME,
        shopify_csv_array)
