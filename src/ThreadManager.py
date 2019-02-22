#!/usr/bin/env python3

"""ThreadManager.py: This file contains the code used to manage the threading aspect of the RhysRoom software."""
import time

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import threading


class ThreadManager(object):
    def __init__(self):
        self.__threads = []

        self.__scheduler = []

    def add_async_thread(self, func, args: tuple = None, start=True):
        """
        Adds a thread to the thread storage and has an option to start the thread.
        :param func: The callback function to execute.
        :param args: The args to pass the function.
        :param start: True if you want the thread to auto start.
        :return: The thread created.
        """
        if args is None:
            args = ()

        thread = threading.Thread(target=func, args=args)

        if start:
            thread.start()

        self.__threads.append(thread)

        return thread

    def add_sync_thread(self, func, args: tuple = None, delay=0):
        task = Task(delay, func, args)

        self.__scheduler.append(task)

    def check_scheduled(self, execute=True):
        for task in self.__scheduler:
            if task.is_elapsed() and execute:
                task.run()


class Task(object):
    def __init__(self, delay: float, func, args: tuple = None):
        self.__start_time = time.time()
        self.__end_time = self.__start_time + delay

        self._func = func

        if args is None:
            args = ()

        self._args = args

    def is_elapsed(self):
        return time.time() > self.__end_time

    def run(self):
        self._func(*self._args)
