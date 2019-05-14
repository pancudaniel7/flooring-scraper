from config import csv_template_dir, url_file_dir
from service.csv import csvService
from service.supplier import stainmasterScrappigService
from transformer import productToShopifyCsvTransformer


# Stainmaster
# Carpet
def stainmaster_carpet_collecting(counter: int):
    products_details = stainmasterScrappigService.get_products_details(stainmasterScrappigService.CARPET_URL, "Carpet",
                                                                       1000, counter,
                                                                       url_file_dir() + stainmasterScrappigService.STAINMASTER_CARPET_CSV_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    products_details.clear()
    csvService.append_csv_array_to_file(
        csv_template_dir() + stainmasterScrappigService.STAINMASTER_CARPET_CSV_FILE_NAME,
        shopify_csv_array)

# Vinyl Luxury
def stainmaster_vinyl_collecting(counter: int):
    products_details = stainmasterScrappigService.get_products_details(stainmasterScrappigService.VINYL_1_URL, "Vinyl Luxury",
                                                                       1000, counter,
                                                                       url_file_dir() + stainmasterScrappigService.STAINMASTER_VINYL_CSV_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    products_details.clear()
    csvService.append_csv_array_to_file(
        csv_template_dir() + stainmasterScrappigService.STAINMASTER_CARPET_CSV_FILE_NAME,
        shopify_csv_array)
