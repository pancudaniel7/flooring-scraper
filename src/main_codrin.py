#!/usr/bin/python3
import config

from controller import tarkettController


def main():
   config.initialise_configurations()
   tarkettController.laminate_collecting()
   tarkettController.vinyl_collecting()
   tarkettController.carpet_collecting()

main()
