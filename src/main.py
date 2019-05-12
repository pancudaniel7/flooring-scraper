#!/usr/bin/python3

from config import initialise_configurations
from controller import bruceController


def main():
    initialise_configurations()
    bruceController.bruce_collecting()


main()
