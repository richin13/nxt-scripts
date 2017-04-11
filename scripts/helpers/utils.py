from __future__ import division
from time import time


def normalize(val, _min, _max):
    return (val - _min) / (_max - _min)


def countdown(initial_time, seconds):
    while time() - initial_time < seconds:
        return False
    return True
