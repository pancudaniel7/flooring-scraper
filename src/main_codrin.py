#!/usr/bin/python3
import config
from controller  import tarkettCotroller


def main():
   config.initialise_configurations()
   tarkettCotroller.tarkett_laminate_collecting()
   tarkettCotroller.tarkett_vinyl_collecting()
   tarkettCotroller.tarkett_carpet_collecting()

main()
