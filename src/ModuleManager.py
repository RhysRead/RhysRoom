#!/usr/bin/env python3

"""ModuleManager.py: This file contains the code for the module managing aspect of the RhysRoom software."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

import os
from importlib.machinery import SourceFileLoader
import threading

MODULE_FOLDER_LOCATION = "/../Modules/"

# Todo: Add logging.


class ModuleManager(object):
    def __init__(self, main, auto_load=True, verbose=True):
        self.__main = main

        self.__file_path = os.path.dirname(os.path.realpath(__file__))
        self.modules = []

        self.__modules_threads = []

        if auto_load:
            count = self.load_modules_from_module_folder()
            if verbose:
                logging.info("{} modules loaded.".format(count))

    def get_module(self, module_name: str):
        """
        Used to retrieve a module from the module manager with the modules name.
        :param module_name:
        :return:
        """
        for module in self.modules:
            if module.get_name() == module_name:
                return module

        return None

    def start_modules(self):
        """
        Used to iterate through and start all loaded modules.
        :return:
        """
        for module in self.modules:
            if not module.run_as_thread:
                module.start()
                continue

            thread = threading.Thread(target=module.start, daemon=True)
            thread.start()
            self.__modules_threads.append(thread)

        for thread in self.__modules_threads:
            thread.join()

    def load_module(self, module_name: str):
        """
        Used to load a single module with its module name.
        :param module_name:
        :return:
        """
        real_module_path = self.__file_path + MODULE_FOLDER_LOCATION + module_name
        module = SourceFileLoader("Module", real_module_path).load_module()
        # Todo: Add exception handling for failure to load modules.
        self.modules.append(module.Module(self.__main))

    def load_modules_from_module_folder(self, verbose=True):
        """
        Used to load modules from the module folder. Will iterate through all files in the directory and attempt to load
        them.
        :return: The integer value of the quantity of modules loaded.
        """
        files = os.listdir(self.__file_path + MODULE_FOLDER_LOCATION)

        count = 0
        for file_name in files:
            # Ensuring that the file is not a directory. Will trigger an error on files with no file type allocated.
            if '.' not in list(file_name) or file_name == "ModuleTemplate.py":
                continue
            self.load_module(file_name)
            count += 1

        return count
