#!/usr/bin/python3


from config import initialise_configurations
from controller import republicController


def main():
    initialise_configurations()
    republicController.vinyl_collecting()
    republicController.laminated_collecting()


main()
