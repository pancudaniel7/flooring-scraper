#!/usr/bin/python3

import os

import csvService
import productToShopifyCsvTransformer
import shawScrapingService
<<<<<<< HEAD
from config import initialise_configurations, logger, csv_template_dir, TEMPLATE_FILE_NAME, url_file_dir
=======
import republicScrapingService
from config import initialise_configurations, logger, csv_template_dir, TEMPLATE_FILE_NAME


def main():
    initialise_configurations()
    logger.info('Start collecting data')

    # Johnson Hardwood
    # products_details = johnsonScrapingService.get_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + johnsonScrapingService.WOOD_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + johnsonScrapingService.WOOD_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # Mohawk Hardwood
    # Wood
    # products_details = mohawkScrapingService.get_wood_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # free_mem(products_details)
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + mohawkScrapingService.WOOD_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + mohawkScrapingService.WOOD_CSV_FILE_NAME,
    #                                     shopify_csv_array)
    #
    # # Vinyl
    # products_details = mohawkScrapingService.get_vinyl_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # free_mem(products_details)
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + mohawkScrapingService.VINYL_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + mohawkScrapingService.VINYL_CSV_FILE_NAME,
    #                                     shopify_csv_array)
    #
    # # Tile
    # products_details = mohawkScrapingService.get_tile_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # free_mem(products_details)
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
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,9
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
>>>>>>> Created republic service for Laminated


<<<<<<< HEAD
def shaw_carpet_collecting():
    products_details = shawScrapingService.get_products_details(shawScrapingService.CARPET_URL, 1000,
                                                                url_file_dir() + shawScrapingService.SHAW_CARPET_URL_FILE_NAME)
=======
    # Mullican
    # products_details = mullicanFlooringScrapingService.get_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + mullicanFlooringScrapingService.MULLICAN_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + mullicanFlooringScrapingService.MULLICAN_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # Fuzion
    # products_details = fuzionScrapingService.get_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + fuzionScrapingService.FUZION_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + fuzionScrapingService.FUZION_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # Bruce
    # products_details = bruceScrapingService.get_products_details()
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + bruceScrapingService.BRUCE_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + bruceScrapingService.BRUCE_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # Shaw
    # hardwood
    # products_details = shawScrapingService.get_products_details(shawScrapingService.HARDWOOD_URL)
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + shawScrapingService.SHAW_HARDWOOD_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + shawScrapingService.SHAW_HARDWOOD_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    # carpet
    # products_details = shawScrapingService.get_products_details(shawScrapingService.CARPET_URL)
    # shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    # csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
    #                           csv_template_dir() + shawScrapingService.SHAW_CARPET_CSV_FILE_NAME)
    # csvService.append_csv_array_to_file(csv_template_dir() + shawScrapingService.SHAW_CARPET_CSV_FILE_NAME,
    #                                     shopify_csv_array)

    #Replublic
    #laminate
    products_details = republicScrapingService.get_products_details(republicScrapingService.LAMINATED_URL)
>>>>>>> Created republic service for Laminated
    shopify_csv_array = [productToShopifyCsvTransformer.product_to_shopify(product) for product in products_details]
    products_details.clear()
    csvService.clean_csv_file(csv_template_dir() + TEMPLATE_FILE_NAME,
                              csv_template_dir() + republicScrapingService.REPUBLIC_LAMINATED_CSV_FILE_NAME)
    csvService.append_csv_array_to_file(csv_template_dir() + republicScrapingService.REPUBLIC_LAMINATED_CSV_FILE_NAME,
                                        shopify_csv_array)
<<<<<<< HEAD


def main():
    initialise_configurations()
    logger.info('Start collecting data')

    shaw_carpet_collecting()

=======
>>>>>>> Created republic service for Laminated
    logger.info('Finish')
    # os.system('poweroff')


main()
