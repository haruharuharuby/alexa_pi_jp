import collections
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
AUDIO_FILE_PATH = './recording.wav'
CHUNK = 320

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
    DETECTING = "DETECTING"
    SPEECHING = "SPEECHING"

    RecorderCaptureState = DETECTING

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream_in = None
        self.ring_buffer = RingBuffer(80000)
        self.no_data_count = 0


    def callback(self, in_data, frame_count, time_info, status):
        if in_data:
            self.no_data_count = 0
        else:
            self.no_data_count = self.no_data_count + 1

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
            stream_callback=callback)


    def is_no_sound():
        return (self.no_data_count == 10)


    def get_data(self):
        return self.ring_buffer.get()


    def resume(self):
        self.stream_in.start_stream()


    def stop(self):
        self.stream_in.stop_stream()


    def terminate(self):
        self.stream_in.close()
        self.audio.terminate()
