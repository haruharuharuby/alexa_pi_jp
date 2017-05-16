#!/usr/bin/env python

import collections
import snowboydetect
import time
import os
import signal
import logging
import RPi.GPIO as GPIO
from device import state

logging.basicConfig()
logger = logging.getLogger("snowboy")
logger.setLevel(logging.INFO)

RESOURCE_FILE = os.path.join(TOP_DIR, "resources/common.res")

class WakeWord(object):
    def __init__(self, decoder_model,
                 resource=RESOURCE_FILE,
                 sensitivity=[],
                 audio_gain=1):

        tm = type(decoder_model)
        ts = type(sensitivity)
        if tm is not list:
            decoder_model = [decoder_model]
        if ts is not list:
            sensitivity = [sensitivity]
        model_str = ",".join(decoder_model)

        self.detector = snowboydetect.SnowboyDetect(
            resource_filename=resource.encode(), model_str=model_str.encode())
        self.detector.SetAudioGain(audio_gain)
        self.num_hotwords = self.detector.NumHotwords()

        if len(decoder_model) > 1 and len(sensitivity) == 1:
            sensitivity = sensitivity*self.num_hotwords
        if len(sensitivity) != 0:
            assert self.num_hotwords == len(sensitivity), \
                "number of hotwords in decoder_model (%d) and sensitivity " \
                "(%d) does not match" % (self.num_hotwords, len(sensitivity))
        sensitivity_str = ",".join([str(t) for t in sensitivity])
        if len(sensitivity) != 0:
            self.detector.SetSensitivity(sensitivity_str.encode())

    def signal_handler(self, signal, frame):
        global interrupted
        interrupted = True


    def interrupt_callback(self):
        global interrupted
        return interrupted


    def detect(self, data=None, detected_callback=None):

        if interrupt_check():
            logger.debug("detect voice return")
            return False

        tc = type(detected_callback)
        if tc is not list:
            detected_callback = [detected_callback]
        if len(detected_callback) == 1 and self.num_hotwords > 1:
            detected_callback *= self.num_hotwords

        assert self.num_hotwords == len(detected_callback), \
            "Error: hotwords in your models (%d) do not match the number of " \
            "callbacks (%d)" % (self.num_hotwords, len(detected_callback))

        if len(data) == 0:
            return False

        ans = self.detector.RunDetection(data)

        if ans == -1:
            message = "Error initializing streams or reading audio data"
        elif ans > 0:
            message = "Keyword " + str(ans) + " detected at time: "
            detected_callback[ans-1]()
            return True
