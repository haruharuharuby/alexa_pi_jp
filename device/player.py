# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import subprocess
import time
import RPi.GPIO as GPIO
import threading
from Queue import Queue
from device_state import DeviceState
import vlc
import pyaudio

v = vlc.Instance()
vlc_player = v.media_player.new()

FILE_NAME = 'response.mp3'

beep_device = pyaudio.PyAudio()

player = Player()

class Player:
    def __init__(self):
        self.__path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))
        self.__avs = Avs(put_audio_to_device=(lambda x: self.play(x)))
        self.__avs.start()
        self.__audio_queue = Queue()
        self.__device_state = DeviceState()
        self.__inp = None
        self.__stop_device = False
        self.__audio_playing = False

    def play(self, audio):
        if audio:
            with open(FILE_NAME, 'wb') as f:
                f.write(audio)
            media = instance.media_new(FILE_NAME)
            vlc_player.set_media(media)
            vlc_player.play()

    def beep(audio):
        w = wave.open(audio, 'rb')
        data = w.readframes(w.getnframes())
        stream_out = beep_device.open(
            format=audio.get_format_from_width(w.getsampwidth()),
            channels=w.getnchannels(),
            rate=w.getframerate(),
            output=True)

        stream_out.write(data)
        time.sleep(0.2)
        stream_out.stop_stream()
        stream_out.close()
        beep_device.terminate()
