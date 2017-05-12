# -*- coding: utf-8 -*-
from google.cloud import speech
from google.cloud import translate
import pyaudio
import boto3
import wave
from time import sleep
import base64

speech_client = speech.Client()
translate_client = translate.Client()
polly_client = boto3.client('polly', region_name='us-west-2')

p1 = pyaudio.PyAudio()
p2 = pyaudio.PyAudio()

# count = p.get_device_count()
# devices = []
# for i in range(count):
#     devices.append(p.get_device_info_by_index(i))
#
# for i, dev in enumerate(devices):
#     print (i, dev['name'])

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
AUDIO_FILE_PATH = './recording.wav'
CHUNK = 1024

RECORDING_TIME = 3

frames = []
def recording_stream_callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return(None, pyaudio.paContinue)


# Problem: We could not play sound asynchronously
# audio = None
# def playing_stream_callback(in_data, frame_count, time_info, status):
#     data = audio.read()
#     return(data, pyaudio.paContinue)


def recognize():
    global audio
    recording_stream = p1.open(
        format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input = True,
        frames_per_buffer = CHUNK,
        stream_callback = recording_stream_callback)

    print("Record %s seconds..." % (RECORDING_TIME))
    sleep(RECORDING_TIME)
    recording_stream.stop_stream()
    recording_stream.close()
    p1.terminate()

    wave_file = wave.open(AUDIO_FILE_PATH, 'wb')
    wave_file.setframerate(RATE)
    wave_file.setsampwidth(p1.get_sample_size(FORMAT))
    wave_file.setnchannels(CHANNELS)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

    with open(AUDIO_FILE_PATH, 'rb') as audio_file:
        sample = speech_client.sample(
            stream=audio_file,
            encoding=speech.Encoding.LINEAR16,
            sample_rate_hertz=RATE)

        results = sample.streaming_recognize(language_code='ja-JP',single_utterance=True)
        for result in results:
            for alternative in result.alternatives:
                print('=' * 20)
                print('transcript: ' + alternative.transcript)
                print('confidence: ' + str(alternative.confidence))

                translation = translate_client.translate(
                    alternative.transcript,
                    target_language='en'
                )
                print('translation: {}'.format(translation['translatedText']))

                translated_audio = polly_client.synthesize_speech(
                    OutputFormat='pcm',
                    Text=translation['translatedText'],
                    VoiceId="Amy"
                )

                if 'AudioStream' in translated_audio:
                    print('ContentType: ' + translated_audio['ContentType'])
                    print('RequestCharacters: ' + translated_audio['RequestCharacters'])

                    # Problem: We could not play sound asynchronously
                    # audio = translated_audio['AudioStream']
                    # audio_stream = p2.open(
                    #     format = FORMAT,
                    #     channels = CHANNELS,
                    #     rate = RATE,
                    #     output = True,
                    #     stream_callback = playing_stream_callback)
                    audio_stream = p2.open(
                        format = FORMAT,
                        channels = CHANNELS,
                        rate = RATE,
                        output = True)
                    audio_stream.write(translated_audio['AudioStream'].read())

                    # Problem: We could not play sound asynchronously
                    # while audio_stream.is_active():
                    #     sleep(0.1)

                    print("Finished playing..")

                    audio_stream.stop_stream()
                    audio_stream.close()
                    p2.terminate()
