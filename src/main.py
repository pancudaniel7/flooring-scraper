#!/usr/bin/python3
import os

from config import initialise_configurations
from controller import shawController


def main():
    initialise_configurations()
    for counter in range(0, 9):
        shawController.shaw_carpet_collecting(counter)
    os.system('poweroff')


main()
