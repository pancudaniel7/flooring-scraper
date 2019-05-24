from config import csv_template_dir, url_file_dir, TEMPLATE_FILE_NAME
from service.csv import csvService
from service.supplier import eleganzaScrappingService
from transformer import productToShopifyCsvTransformer


def collecting():
    product_details = eleganzaScrappingService.get_products_details(eleganzaScrappingService.TILE_URLS, 'Tile',
                                                                    url_file_dir() + eleganzaScrappingService.TILE_URL_FILE_NAME)
    csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
                              csv_template_dir() + eleganzaScrappingService.TILE_CSV_FILE_NAME)
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in product_details]
    product_details.clear()
    csvService.append_csv_array_to_file(
        csv_template_dir() + eleganzaScrappingService.TILE_CSV_FILE_NAME, shopify_csv_array)
