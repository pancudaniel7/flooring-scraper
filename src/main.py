from src.config import logger, initialise_configurations, csv_template_dir, TEMPLATE_FILE_NAME
from src.service.shopify import csvService
from src.service.supplier import knoasScrapingService, regalScrapingService, mohawkScrapingService, \
    johnsonScrapingService, lwScrapingService, eagleFlooringScrapingService
from src.transformer import productToShopifyCsvTransformer


def main():
    logger.info('Start collecting data')
    initialise_configurations()

    # Johnson Hardwood
    # products_details = johnsonScrapingService.get_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + mohawkScrapingService.WOOD_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + johnsonScrapingService.CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # Mohawk Hardwood
    # Wood
    # products_details = mohawkScrapingService.get_wood_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + mohawkScrapingService.WOOD_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + mohawkScrapingService.WOOD_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # Vinyl
    # products_details = mohawkScrapingService.get_vinyl_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + mohawkScrapingService.VINYL_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + mohawkScrapingService.VINYL_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # Tile
    # products_details = mohawkScrapingService.get_tile_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + mohawkScrapingService.TILE_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + mohawkScrapingService.TILE_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # Regal Hardwood
    # products_details = regalScrapingService.get_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + regalScrapingService.REGAL_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + regalScrapingService.REGAL_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # Knoas
    # products_details = knoasScrapingService.get_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + knoasScrapingService.KNOAS_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + knoasScrapingService.KNOAS_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # Lw
    # products_details = lwScrapingService.get_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + lwScrapingService.LW_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + lwScrapingService.LW_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # Eagle creek
    # products_details = eagleFlooringScrapingService.get_hardwood_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + eagleFlooringScrapingService.EAGLE_HARDWOOD_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + eagleFlooringScrapingService.EAGLE_HARDWOOD_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # products_details = eagleFlooringScrapingService.get_laminate_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + eagleFlooringScrapingService.EAGLE_LAMINATE_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + eagleFlooringScrapingService.EAGLE_LAMINATE_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # products_details = eagleFlooringScrapingService.get_vinyl_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + eagleFlooringScrapingService.EAGLE_VINYL_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + eagleFlooringScrapingService.EAGLE_VINYL_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    logger.info('Finish')


main()
