#!/usr/bin/python3


from config import initialise_configurations
from controller import urbanController


def main():
    initialise_configurations()
    urbanController.collecting()


main()
