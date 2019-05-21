#!/usr/bin/python3
import os

from config import initialise_configurations
from controller import tarkettController, fuzionController


def main():
    initialise_configurations()
    fuzionController.collecting()


main()
