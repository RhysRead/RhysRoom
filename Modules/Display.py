#!/usr/bin/env python3

"""ModuleTemplate.py: This file contains an example for the creation of a module for the RhysRoom software."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging
import tkinter as tk
import random
import string
import time
import psutil

from Modules.ModuleTemplate import ModuleTemplate


class Module(ModuleTemplate):
    def __init__(self, main):
        super().__init__(main)

    def start(self):
        logging.info('Starting GUI.')
        display = Display(self.main)

        self.main.thread_manager.add_async_thread(display.random_loop)
        self.main.thread_manager.add_async_thread(display.battery_loop)

        self.main.thread_manager.add_sync_thread(display.start)

    def get_name(self):
        return "Display"


class Display(object):
    def __init__(self, main):
        self.active = True

        self.main = main

        self.__root = tk.Tk()
        self.__root.title('RhysRoom software')
        self.__root.geometry('500x500')

        self.__frame = tk.Frame(self.__root)
        self.__frame.pack()

        self.__labels = [tk.Label(self.__frame, text=random_text(25)) for i in range(0, 5)]
        [i.pack() for i in self.__labels]

        self.__battery_level = tk.Label(self.__frame,
                                        text='')
        self.__battery_level.pack()

        button = tk.Button(self.__frame,
                           text='QUIT',
                           fg='red',
                           command=self.__exit)
        button.pack()

    def start(self):
        self.__root.mainloop()

    def __update(self):
        if not self.active:
            return
        self.__root.update()

    def random_loop(self):
        # Todo: Research threading module a bit more to be more confident with threads and cores
        while self.active:
            self.__update()

            # Broad exception clause to handle unexpected closure
            try:
                [i.config(text=random_text(25)) for i in self.__labels]
            except:
                pass
            time.sleep(0.01)

    def battery_loop(self):
        while self.active:
            self.__update()

            # Broad exception clause to handle unexpected closure
            try:
                battery = psutil.sensors_battery()
                self.__battery_level.config(text=str(battery.percent))
            except:
                pass

    def __exit(self):
        self.active = False
        self.main.active = False
        self.__root.destroy()


def random_text(length):
    return ''.join([random.choice(string.ascii_letters) for i in range(0, length)])
