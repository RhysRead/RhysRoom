#!/usr/bin/env python3

"""ModuleTemplate.py: This file contains the abstract class for a module for the RhysRoom software."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging

from abc import ABC, abstractmethod


class ModuleTemplate(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def start(self):
        pass
