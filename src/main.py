#!/usr/bin/python3


from config import initialise_configurations
from controller import americanoController, shawController, fuzionController
from service.supplier import shawScrapingService


def main():
    initialise_configurations()

    americanoController.collecting()

    shawController.collecting(shawScrapingService.VINYL_URL, shawScrapingService.SHAW_VINYL_CSV_FILE_NAME)
    shawController.collecting(shawScrapingService.LAMINATE_URL, shawScrapingService.SHAW_LAMINATE_CSV_FILE_NAME)

    fuzionController.collecting()


main()
