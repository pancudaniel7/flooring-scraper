from src.Config import logger, initialise_configurations, csv_template_dir
from src.service.supplier.JohnsonScrapingService import get_products_details, JOHNSOON_CSV_FILE_NAME
from src.service.shopify.CsvService import append_csv_array_to_file
from src.transformer.ProductToShoppifyCsvTransformer import product_to_shopify


def main():
    logger.info('Start collecting data')
    initialise_configurations()
    # Johnson Hardwood
    products_details = get_products_details()
    shoppify_csv_array = [product_to_shopify(product) for product in products_details]
    append_csv_array_to_file(csv_template_dir() + JOHNSOON_CSV_FILE_NAME, shoppify_csv_array)
    logger.info('Finish')


main()
