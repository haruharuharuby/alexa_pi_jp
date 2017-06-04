# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import time
from Queue import Queue
from device import vlc
import pyaudio
import wave
import subprocess

v = vlc.Instance()
vlc_player = v.media_player_new()

FILE_NAME = 'response.mp3'
TMP_FILE_NAME = 'tmp_response.wav'

beep_device = pyaudio.PyAudio()

class Player:

    def play(self, audio, convert=True):
        if not audio:
            return
        with open(FILE_NAME, 'wb') as f:
            f.write(audio)
        media = v.media_new(FILE_NAME)
        vlc_player.set_media(media)
        vlc_player.play()

    def beep(self, audio):
        w = wave.open(audio, 'rb')
        data = w.readframes(w.getnframes())
        stream_out = beep_device.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            output=True)

        stream_out.write(data)
        time.sleep(0.2)
        stream_out.stop_stream()
        stream_out.close()
        beep_device.terminate()
