#!/usr/bin/python3

from config import initialise_configurations
from controller import marazziController


def main():
    initialise_configurations()
    marazziController.collecting()


main()
