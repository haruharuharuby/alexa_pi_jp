import os
import time
import wakeword
from device import player, recorder
from alexa import avs
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
DETECT_DING = os.path.join(TOP_DIR, "resources/ding.wav")
DETECT_DONG = os.path.join(TOP_DIR, "resources/dong.wav")
MODELS = ["resources/alexa.umdl", "resources/stop.pmdl"]
SLEEP_TIME = 0.01

player = player.Player()
recorder = recorder.Recorder()

hot_words = wakeword.WakeWord(decoder_model=MODELS)
avs = avs.Avs(player)

running = True


def detected():
    print("DETECTED")

def run():
    recorder.open()
    while running:
        data = recorder.get_data()
        if len(data) != 0:
            avs.send(data)
        #time.sleep(0.01)


try:
    run()
except KeyboardInterrupt:
    print("ctrl-c")
    running = False
finally:
    print("stopped")
    avs.close()
    recorder.stop()
    recorder.terminate()
