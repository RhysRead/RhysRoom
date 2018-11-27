#!/usr/bin/env python3

"""ModuleTemplate.py: This file contains an example for the creation of a module for the RhysRoom software."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

from Modules.ModuleTemplate import ModuleTemplate


class Module(ModuleTemplate):
    def __init__(self):
        super().__init__()

    def start(self):
        print("Hello world!")
