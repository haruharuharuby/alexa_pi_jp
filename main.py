import sys
import os
import wave
import pyaudio
import time
import signal
import wakeword
from recorder import recorder


try:
    recorder.open()
    wake.start_detection()
except KeyboardInterrupt:
    print("ctrl-c")
finally:
    wake.stop_detection()
