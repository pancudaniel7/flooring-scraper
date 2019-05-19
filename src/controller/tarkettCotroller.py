import config
from service.csv import csvService
from service.supplier import tarkettScrapingService
from transformer import productToShopifyCsvTransformer


def laminate_collecting():
    product_details = tarkettScrapingService.get_products_details(tarkettScrapingService.LAMINATED_URL, "Laminated")
    csvService.clean_csv_file(config.csv_template_dir() + config.TEMPLATE_FILE_NAME,
                              config.csv_template_dir() + tarkettScrapingService.TARKETT_LAMINATED_CSV_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in product_details]
    product_details.clear()
    csvService.append_csv_array_to_file(
        config.csv_template_dir() + tarkettScrapingService.TARKETT_LAMINATED_CSV_FILE_NAME,
        shopify_csv_array)


def vinyl_collecting():
    product_details = tarkettScrapingService.get_products_details(tarkettScrapingService.VINYL_1_URL, "Vinyl")
    product_details.extend(tarkettScrapingService.get_products_details(tarkettScrapingService.VINYL_2_URL, "Vinyl"))
    csvService.clean_csv_file(config.csv_template_dir() + config.TEMPLATE_FILE_NAME,
                              config.csv_template_dir() + tarkettScrapingService.TARKETT_VINYL_CSV_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in product_details]
    product_details.clear()
    csvService.append_csv_array_to_file(config.csv_template_dir() + tarkettScrapingService.TARKETT_VINYL_CSV_FILE_NAME,
                                        shopify_csv_array)


def carpet_collecting():
    product_details = tarkettScrapingService.get_products_details(tarkettScrapingService.CARPET_URL, "Carpet")
    csvService.clean_csv_file(config.csv_template_dir() + config.TEMPLATE_FILE_NAME,
                              config.csv_template_dir() + tarkettScrapingService.TARKETT_CARPET_CSV_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in product_details]
    product_details.clear()
    csvService.append_csv_array_to_file(config.csv_template_dir() + tarkettScrapingService.TARKETT_CARPET_CSV_FILE_NAME,
                                        shopify_csv_array)
