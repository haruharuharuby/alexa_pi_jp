import os
import time
import wakeword
from translation import speech 
from device import player, recorder
from alexa import avs

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
DETECT_DING = os.path.join(TOP_DIR, "resources/ding.wav")
DETECT_DONG = os.path.join(TOP_DIR, "resources/dong.wav")

player = player.Player()
recorder = recorder.Recorder()

avs = avs.Avs(player)
wake = wakeword.WakeWord(sensitivity=0.5)

running = True

def run():
    recorder.open()
    while running:
        data = recorder.get_data()
        if len(data) != 0:
            ans = wake.detect(data)
            print(ans)
            if ans is None:
                translated_voice = speech.recognize(data)
                audio = avs.send(translated_voice)
                output_voice = speech.recognize(audio, src_lang_code='en-US', to_lang='ja', convert=True, output='mp3')
                player.play(output_voice)
            elif ans == 1:
                print('Detected, Alexa')
            elif ans == 2:
                print('Call Going Out Skill')
                with open('resources/ask_my_home_keeper.wav', 'rb') as inf:
                    voice_trigger = inf.read()
                    audio = avs.send(voice_trigger)
                    output_voice = speech.recognize(audio, src_lang_code='en-US', to_lang='ja', convert=True, output='mp3')
                    player.play(output_voice)
            elif ans == 3:
                print('Call Homecomming Skill')
                with open('resources/homecoming.wav', 'rb') as inf:
                    voice_trigger = inf.read()
                    audio = avs.send(voice_trigger)
                    player.play(audio)
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
