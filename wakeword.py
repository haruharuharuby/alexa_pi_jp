#!/usr/bin/env python

import collections
import snowboydetect
import time
import os
import signal
import logging
import RPi.GPIO as GPIO

logging.basicConfig()
logger = logging.getLogger("snowboy")
logger.setLevel(logging.INFO)

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_FILE = os.path.join(TOP_DIR, "resources/common.res")
HOTWORDS = ['resources/alexa.umdl','resources/ittekimasu.pmdl','resources/tadaima.pmdl']

class WakeWord(object):
    def __init__(self, resource=RESOURCE_FILE,
                 sensitivity=[],
                 audio_gain=1):

        ts = type(sensitivity)
        if ts is not list:
            sensitivity = [sensitivity]
        model_str = ",".join(HOTWORDS)

        self.detector = snowboydetect.SnowboyDetect(resource, model_str)
        self.detector.SetAudioGain(audio_gain)
        self.num_hotwords = self.detector.NumHotwords()

        if len(HOTWORDS) > 1 and len(sensitivity) == 1:
            sensitivity = sensitivity*self.num_hotwords
        if len(sensitivity) != 0:
            assert self.num_hotwords == len(sensitivity), \
                "number of hotwords in decoder_model (%d) and sensitivity " \
                "(%d) does not match" % (self.num_hotwords, len(sensitivity))
        sensitivity_str = ",".join([str(t) for t in sensitivity])
        if len(sensitivity) != 0:
            self.detector.SetSensitivity(sensitivity_str)


    def detect(self, data=None):

        if len(data) == 0:
            return -1 

        ans = self.detector.RunDetection(data)

        if ans == -1:
            message = "Error initializing streams or reading audio data"
            print(message)
            return ans
        elif ans > 0:
            message = "Keyword " + str(ans) + " detected at time: "
            return ans 
