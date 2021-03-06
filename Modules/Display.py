#!/usr/bin/env python3

"""ModuleTemplate.py: This file contains an example for the creation of a module for the RhysRoom software."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import logging
import tkinter as tk
import time
import datetime

from Modules.ModuleTemplate import ModuleTemplate

# EVENT_CAP defines the maximum amount of events to be listed in the event box at once
EVENT_CAP = 10


class Module(ModuleTemplate):
    def __init__(self, main):
        super().__init__(main)

    def start(self):
        logging.info('Starting GUI.')
        display = Display(self.main)

        self.main.thread_manager.add_sync_thread(display.start)

    def get_name(self):
        return "Display"


class Display(object):
    def __init__(self, main):
        self.active = True

        self.main = main

        self.__root = tk.Tk()
        self.__root.title('RhysRoom software')

        self.start_time = time.time()

        # Label

        self.__label0 = tk.Label(self.__root, text='RhysRoom Software', font='Helvetica 18 bold')
        self.__label0.grid(row=0, column=1)

        self.__label1 = tk.Label(self.__root, text='Events:', font='Helvetica 16 bold')
        self.__label1.grid(row=1, column=0)

        self.__label2 = tk.Label(self.__root, text='Active Modules:', font='Helvetica 16 bold')
        self.__label2.grid(row=1, column=1)

        self.__label3 = tk.Label(self.__root, text='Disabled Modules:', font='Helvetica 16 bold')
        self.__label3.grid(row=1, column=2)

        # Dynamic label

        self.time0 = tk.Label(self.__root,
                              text=time.strftime('%H:%M:%S'),
                              font='Helvetica 100 bold',
                              fg='Navy')
        self.main.thread_manager.add_async_thread(time_loop, args=(self,))
        self.time0.grid(row=2, column=4)

        self.date0 = tk.Label(self.__root,
                              text=datetime.datetime.today().strftime('%Y-%m-%d'),
                              font='Helvetica 60',
                              fg='Navy')
        self.main.thread_manager.add_async_thread(date_loop, args=(self,))
        self.date0.grid(row=3, column=4)

        self.day0 = tk.Label(self.__root,
                             text=datetime.datetime.now().strftime('%A'),
                             font='Helvetica 50',
                             fg='Blue')
        self.main.thread_manager.add_async_thread(day_loop, args=(self,))
        self.day0.grid(row=4, column=4)

        self.uptime0 = tk.Label(self.__root,
                                text='',
                                font='Helvetica 20',
                                fg='Navy')
        self.main.thread_manager.add_async_thread(uptime_loop, args=(self,))
        self.uptime0.grid(row=3, column=1)

        # Dynamic listbox

        self.__events0 = tk.Listbox(self.__root)
        self.__events0.grid(row=2, column=0)
        # Todo: Test if event limiter even works
        self.__events0_amount = 0

        self.__active_modules0 = tk.Listbox(self.__root)
        self.__active_modules0.grid(row=2, column=1)

        self.__disabled_modules0 = tk.Listbox(self.__root)
        self.__disabled_modules0.grid(row=2, column=2)

        # Updates active modules listbox
        for module in main.module_manager.modules:
            self.add_active_module(module.get_name())

    def start(self):
        self.__root.mainloop()
        self.__exit()

    def add_active_module(self, module_name: str):
        self.__active_modules0.insert(0, module_name)
        self.update()

    def add_event(self, event_text: str):
        # Todo: Integrate limit into this
        self.__events0.insert(0, event_text)

        self.__events0_amount += 1

        if self.__events0_amount > EVENT_CAP:
            self.__events0.delete(EVENT_CAP)
            self.__events0_amount -= 1

        self.update()

    def update(self):
        if not self.active:
            return
        self.__root.update()

    def __exit(self):
        self.active = False
        self.main.active = False


# Dynamic label methods

# Todo: Re-do this code so that it's not spaghetti, it's a bit hacky right now
def time_loop(display_module: Display):
    while display_module.main.active:
        display_module.time0.config(text=time.strftime('%H:%M:%S'))
        time.sleep(0.01)
        display_module.update()


def date_loop(display_module: Display):
    while display_module.main.active:
        display_module.date0.config(text=datetime.datetime.today().strftime('%d-%m-%Y'))
        time.sleep(60)
        display_module.update()


def day_loop(display_module: Display):
    display_module.day0.config(text=datetime.datetime.now().strftime('%A'))
    time.sleep(3600)
    display_module.update()


def uptime_loop(display_module: Display):
    while display_module.main.active:
        elapsed_time = time.time() - display_module.start_time
        # Todo: Fix minutes exceeding max limit
        unformatted_time = [elapsed_time // 3600, elapsed_time // 60, elapsed_time % 60]

        # Removes issue of minutes value being > 60
        if unformatted_time[1] > 60:
            unformatted_time[1] = unformatted_time[1] % 60

        formatted_time = ':'.join([str(round(i)) for i in unformatted_time])

        display_module.uptime0.config(text='Uptime {}'.format(formatted_time))

        time.sleep(1)
