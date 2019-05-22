#!/usr/bin/python3


from config import initialise_configurations
from controller import tarkettController


def main():
    initialise_configurations()
    tarkettController.laminate_collecting()
    tarkettController.vinyl_collecting()
    tarkettController.carpet_collecting()


main()
