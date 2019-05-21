#!/usr/bin/python3
import config
from controller import stainmasterController


def main():
    config.initialise_configurations()
    for counter in range(0, 9):
        stainmasterController.stainmaster_carpet_collecting(counter)
    stainmasterController.stainmaster_vinyl_collecting(0)

main()
