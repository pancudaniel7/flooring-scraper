from src.Config import logger, initialise_configurations, csv_template_dir
from src.service.shopify import CsvService
from src.service.supplier import MohawkScrapingService, JohnsonScrapingService


def main():
    logger.info('Start collecting data')
    initialise_configurations()

    # Johnson Hardwood
    products_details = JohnsonScrapingService.get_products_details()
    shoppify_csv_array = [JohnsonScrapingService.product_to_shopify(product) for product in products_details]
    CsvService.append_csv_array_to_file(csv_template_dir() + JohnsonScrapingService.CSV_FILE_NAME,
                                        shoppify_csv_array)

    # # Mohawk Hardwood
    # MohawkScrapingService.get_wood_products_details()

    logger.info('Finish')


main()
