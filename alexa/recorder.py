#!/usr/bin/env python

import collections
import time
import os
import signal
import logging
import RPi.GPIO as GPIO
from recorder import recorder
from avs import avs

class Recorder(object):
    def __init__(self):
        recorder.resume()

    def start():
        while(!recorder.is_no_sound()):
            sleep(0.03)
        data = recorder.get_data()
        avs.put_audio(data)
