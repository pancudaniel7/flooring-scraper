#!/usr/bin/python3

from config import initialise_configurations
from controller import prestigeController


def main():
    initialise_configurations()
    prestigeController.collecting()


main()
