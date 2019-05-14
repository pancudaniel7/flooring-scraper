#!/usr/bin/python3
import config
from controller import stainmasterController


def main():
    config.initialise_configurations()
    stainmasterController.stainmaster_carpet_collecting(5)


main()
