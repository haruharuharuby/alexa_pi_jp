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

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
AUDIO_FILE_PATH = './recording.wav'
CHUNK = 1024


def recognize(data):

    wave_file = wave.open(AUDIO_FILE_PATH, 'wb')
    wave_file.setframerate(RATE)
    wave_file.setsampwidth(2)
    wave_file.setnchannels(CHANNELS)
    wave_file.writeframes(data)
    wave_file.close()

    with open(AUDIO_FILE_PATH, 'rb') as audio_file:
        sample = speech_client.sample(
            stream=audio_file,
            encoding=speech.Encoding.LINEAR16,
            sample_rate=RATE)

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

                    return translated_audio['AudioStream'].read()
        return None
