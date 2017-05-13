#!/usr/bin/env python

import collections
import snowboydetect
import time
import os
import signal
import logging
import RPi.GPIO as GPIO
from recorder import recorder

logging.basicConfig()
logger = logging.getLogger("snowboy")
logger.setLevel(logging.INFO)
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
DETECT_DING = os.path.join(TOP_DIR, "resources/ding.wav")
DETECT_DONG = os.path.join(TOP_DIR, "resources/dong.wav")
RESOURCE_FILE = os.path.join(TOP_DIR, "resources/common.res")
MODELS = ["resources/alexa.umdl", "resources/Stop.pmdl"]

#
# interrupted
#
def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


#
# Wakeword detection call back methods
#
def alexa():
    Player.beep(DETECT_DING)
    print("[STATE:WAKE] detected alexa")


def stop():
    Player.beep(DETECT_DONG)
    print("[STATE:WAKE] detected stop")


callbacks = [alexa, stop]

def start_detection():
    detector = WakeWordDetector(models, sensitivity=0.5)
    detector.start(detected_callback=callbacks, interrupt_check=interrupt_callback, sleep_time=0.03)


def stop_detection():
    detector.terminate()


class WakeWordDetector(object):
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

        self.running = True


    def start(self, detected_callback=None,
              interrupt_check=lambda: False,
              sleep_time=0.03):

        if interrupt_check():
            logger.debug("detect voice return")
            return

        tc = type(detected_callback)
        if tc is not list:
            detected_callback = [detected_callback]
        if len(detected_callback) == 1 and self.num_hotwords > 1:
            detected_callback *= self.num_hotwords

        assert self.num_hotwords == len(detected_callback), \
            "Error: hotwords in your models (%d) do not match the number of " \
            "callbacks (%d)" % (self.num_hotwords, len(detected_callback))

        logger.debug("detecting...")

        while self.running:
            if interrupt_check():
                logger.debug("detect voice break")
                break

            data = self.recorder.get_data()
            if len(data) == 0:
                time.sleep(sleep_time)
                continue
            ans = self.detector.RunDetection(data)
            time.sleep(sleep_time)

            if ans == -1:
                message = "Error initializing streams or reading audio data"
            elif ans > 0:
                message = "Keyword " + str(ans) + " detected at time: "
                recorder.stop()
                detected_callback[ans-1]()


        logger.debug("Stopped")


    def terminate(self):
        self.running = False
