from src.Config import logger, initialise_configurations
from src.service.JohnsonScrapingService import get_products_details


def main():

        initialise_configurations()
        get_products_details()



main()
