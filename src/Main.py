#!/usr/bin/env python3

"""Main.py: This file contains the main code for the execution of the RhysRoom software."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging
import os

from ModuleManager import ModuleManager
from ThreadManager import ThreadManager

logging.basicConfig(level=logging.DEBUG)


class Main(object):
    def __init__(self):
        self.module_manager = ModuleManager(self)
        self.thread_manager = ThreadManager()

        self.active = True

    def start(self):
        self.module_manager.start_modules()

        while self.active:
            self.thread_manager.check_scheduled()

            if not self.active:
                self.__exit()

    def __exit(self):
        self.thread_manager.stop_all()
        # Hacky way to get a clean exit when exiting through the display exit button:
        os._exit(0)


if __name__ == "__main__":
    main = Main()
    main.start()
