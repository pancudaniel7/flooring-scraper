#!/usr/bin/python3
from config import initialise_configurations
from controller import tarkettCotroller


def main():
    initialise_configurations()
    tarkettCotroller.laminate_collecting()
    tarkettCotroller.vinyl_collecting()
    tarkettCotroller.carpet_collecting()


main()
