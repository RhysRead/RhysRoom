#!/usr/bin/env python3

"""Main.py: This file contains the main code for the execution of the RhysRoom software."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

from ModuleManager import ModuleManager

logging.basicConfig(level=logging.DEBUG)


class Main(object):
    def __init__(self):
        self.__module_manager = ModuleManager()

    def start(self):
        self.__module_manager.start_modules()


if __name__ == "__main__":
    main = Main()
    main.start()
