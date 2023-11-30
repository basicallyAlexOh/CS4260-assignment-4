"""
timer.py
Classes: Timer
Taken from https://stackoverflow.com/questions/60026296/how-to-make-a-pausable-timer-in-python
"""
from datetime import datetime
import time


class Timer:
    """
    timer.start() - should start the timer
    timer.pause() - should pause the timer
    timer.resume() - should resume the timer
    timer.get() - should return the current time
    """

    def __init__(self):
        self.__timestarted = None
        self.__timepaused = None
        self.paused = False

    def start(self):
        """ Starts an internal timer by recording the current time """
        self.__timestarted = datetime.now()

    def pause(self):
        """ Pauses the timer """
        if self.__timestarted is None:
            raise ValueError("Timer not started")
        if self.paused:
            raise ValueError("Timer is already paused")
        self.__timepaused = datetime.now()
        self.paused = True

    def resume(self):
        """ Resumes the timer by adding the pause time to the start time """
        if self.__timestarted is None:
            raise ValueError("Timer not started")
        if not self.paused:
            raise ValueError("Timer is not paused")
        pausetime = datetime.now() - self.__timepaused
        self.__timestarted = self.__timestarted + pausetime
        self.paused = False

    def get(self):
        """ Returns a timedelta object showing the amount of time
            elapsed since the start time, less any pauses """
        if self.__timestarted is None:
            raise ValueError("Timer not started")
        if self.paused:
            return self.__timepaused - self.__timestarted
        else:
            return datetime.now() - self.__timestarted