import collections
import pyaudio
import audioop
import time
import math

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024 
THRESHOLD = 2500

class RingBuffer(object):
    """Ring buffer to hold audio from PortAudio"""
    def __init__(self, size = 4096):
        self._buf = collections.deque(maxlen=size)


    def extend(self, data):
        """Adds data to the end of buffer"""
        self._buf.extend(data)

    
    def get(self):
        """Retrieves data from the beginning of buffer and clears it"""
        tmp = bytes(bytearray(self._buf))
        self._buf.clear()
        return tmp


class Recorder(object):

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream_in = None
        self.ring_buffer = RingBuffer(80000)

 
    def callback(self, in_data, frame_count, time_info, status):
        self.ring_buffer.extend(in_data)
        data_len = chr(0) * len(in_data)
        return (data_len, pyaudio.paContinue)


    def open(self):
        self.stream_in = self.audio.open(
            input=True,
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            frames_per_buffer=CHUNK,
            stream_callback=self.callback)


    def get_data(self):
        finished = False
        started = False
        voice = b''
        rel = RATE / CHUNK
        silence_detection = collections.deque(maxlen=rel)   
        while(not finished):
            data = self.ring_buffer.get()
            #print(data)
            silence_detection.append(math.sqrt(abs(audioop.avg(data, 4))))
            if(sum([x > THRESHOLD for x in silence_detection]) > 0):
                if(not started):
                    print("[RECORDER:STATE] recording started.")
                    started = True
                voice = b''.join([voice, data])
            elif(started):
                print("[RECORDER:STATE] recording finished")
                started = False
                finished = True 
            time.sleep(0.03) 
        return voice


    def resume(self):
        self.stream_in.start_stream()


    def stop(self):
        if self.stream_in:
            self.stream_in.stop_stream()


    def terminate(self):
        if self.stream_in:
            self.stream_in.close()
        self.audio.terminate()
