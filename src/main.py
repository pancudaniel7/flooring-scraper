#!/usr/bin/python3


from config import initialise_configurations
from controller import eleganzaController


def main():
    initialise_configurations()
    eleganzaController.collecting()

main()
