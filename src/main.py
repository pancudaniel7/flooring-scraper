#!/usr/bin/python3
import os

from config import initialise_configurations
from controller import bruceController


def main():
    initialise_configurations()
    bruceController.bruce_collecting()
    # os.system('poweroff')


main()
