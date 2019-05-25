from config import csv_template_dir, url_file_dir, TEMPLATE_FILE_NAME
from service.csv import csvService
from service.supplier import republicScrappingService
from transformer import productToShopifyCsvTransformer


def laminated_collecting():
    product_details = republicScrappingService.get_products_details(republicScrappingService.LAMINATED_URL, 'Laminated',
                                                                    url_file_dir() + republicScrappingService.LAMINATED_URL_FILE_NAME)
    csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
                              csv_template_dir() + republicScrappingService.LAMINATED_CSV_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in product_details]
    product_details.clear()
    csvService.append_csv_array_to_file(
        csv_template_dir() + republicScrappingService.LAMINATED_CSV_FILE_NAME, shopify_csv_array)


def vinyl_collecting():
    product_details = republicScrappingService.get_products_details(republicScrappingService.VINYL_URL, 'Vinyl',
                                                                    url_file_dir() + republicScrappingService.VINYL_URL_FILE_NAME)
    csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
                              csv_template_dir() + republicScrappingService.VINYL_CSV_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in product_details]
    product_details.clear()
    csvService.append_csv_array_to_file(
        csv_template_dir() + republicScrappingService.VINYL_CSV_FILE_NAME, shopify_csv_array)
