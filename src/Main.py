from src.Config import logger, initialise_configurations
from src.service.JohnsonScrapingService import get_all_products_urls


def main():
    initialise_configurations()
    print(get_all_products_urls())


main()
