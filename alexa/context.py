# AVS Contexts
# https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/reference/context#additional-interfaces

class AudioPlayer:
    IDLE = "IDLE"
    PLAYING = "PLAYING"
    STOPPED = "STOPPED"
    PAUSED = "PAUSED"
    BUFFER_UNDERRUN = "BUFFER_UNDERRUN"
    FINISHED = "FINISHED"

    PlaybackState = {
        "header": {
            "namespace": "AudioPlayer",
            "name": "PlaybackState"
        },
        "payload": {
            "token": "",
            "offsetInMilliseconds": 0,
            "playerActivity": IDLE
        }
    }


class Alerts:
    TIMER = "TIMER"
    ALERT = "ALERT"
    AlertsState = {
        "header": {
            "namespace": "Alerts",
            "name": "AlertsState"
        },
        "payload": {
            "allAlerts": [
                              {
                    "token": "",
                    "type": TIMER,
                    "scheduledTime": ""
                }
            ],
            "activeAlerts": [
                              {
                    "token": "",
                    "type": TIMER,
                    "scheduledTime": ""
                }
            ]
        }
    }


class Speaker:
    VolumeState = {
        "header": {
            "namespace": "Speaker",
            "name": "VolumeState"
        },
        "payload": {
            "volume": 0,
            "muted": False
        }
    }


class SpeechSynthesizer:
    PLAYING = "PLAYING"
    FINISHED = "FINISHED"

    SpeechState = {
        "header": {
            "namespace": "SpeechSynthesizer",
            "name": "SpeechState"
        },
        "payload": {
            "token": "",
            "offsetInMilliseconds": 0,
            "playerActivity": PLAYING
        }
    }
