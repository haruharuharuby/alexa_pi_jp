import os
import time
import wakeword
from device import player, recorder
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
DETECT_DING = os.path.join(TOP_DIR, "resources/ding.wav")
DETECT_DONG = os.path.join(TOP_DIR, "resources/dong.wav")
MODELS = ["resources/alexa.umdl", "resources/stop.pmdl"]
SLEEP_TIME = 0.01

player = player.Player()
recorder = recorder.Recorder()

hot_words = wakeword.WakeWord(decoder_model=MODELS)
# avs = alexa.Avs(recorder)

running = True


# callback when "alexa" detected.
def alexa():
    player.beep(DETECT_DING)
    print("[STATE:CONTROLLER] detected alexa")



# callback when "stop" detected.
def stop():
    player.beep(DETECT_DONG)
    print("[STATE:CONTROLLER] detect stop")
    recorder.terminate()
    player.terminate()


def run():
    recorder.open()
    while running:
        data = recorder.get_data()
        hot_words.detect(data=data, detected_callback=[alexa, stop])
        time.sleep(SLEEP_TIME)



try:
    run()
except KeyboardInterrupt:
    print("ctrl-c")
    running = False
finally:
    print("stopped")
    recorder.stop()
    recorder.terminate()
