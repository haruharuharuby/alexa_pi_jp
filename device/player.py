# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import time
from Queue import Queue
from device import vlc
import pyaudio
import wave

v = vlc.Instance()
vlc_player = v.media_player_new()

FILE_NAME = 'response.mp3'

beep_device = pyaudio.PyAudio()

class Player:

    def play(self, audio):
        if audio:
            with open(FILE_NAME, 'wb') as f:
                f.write(audio)
            media = instance.media_new(FILE_NAME)
            vlc_player.set_media(media)
            vlc_player.play()

    def beep(self, audio):
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
