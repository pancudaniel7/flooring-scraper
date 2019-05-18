#!/usr/bin/python3
import os

from config import initialise_configurations
from controller import shawController, daltileController


def main():
    initialise_configurations()
    daltileController.collecting()


main()
