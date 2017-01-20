# python3 -m pip install pocketsphinx

from speech_recognition import Microphone, Recognizer, AudioData
from requests import get
import json
import pprint

prettyprinter = pprint.PrettyPrinter(indent=4)

HIGH = 4000
LOW = 1000
SENSITIVITY = HIGH
some_structure = None
voice_function = None





def asynch_listener_fn(recognizer_instance, audio_data):
    global some_structure, voice_function, prettyprinter

    print("Performing Sphinx Speech to Text asynchronously")
    try:
        text_from_audio = \
            recognizer_instance.recognize_sphinx( \
                audio_data, show_all = False)
    except Exception as e:
        print(
            "Exception in recognizer: " + str(e))
        text_from_audio = None

    print("Text recognized:\n\t", end="")
    print(text_from_audio)
    print("Sending HTTP request to API AI")
    some_structure = \
        get('https://api.api.ai/v1/query?v=20150910&query=%s&lang=en&sessionId=1234567890' % text_from_audio,
            headers={
                'language-tag'  : 'en',
                'Authorization' : 'Bearer e4099166fd7a41218ba851d21e6866f5',
                'Content-Type'  : 'application/json; charset=utf-8'
            }
        )

    print("Got structure back:")
    try: prettyprinter.pprint(some_structure.json())
    except: print("Could not print JSON result.")

    try:
        voice_function = eval(some_structure.json()['result']['metadata']['intentName'])
    except Exception as err:
        print("Not a valid voice function", voice_function)
        print("Exception: {0}".format(err))
        voice_function = None

    return text_from_audio

# developer:    cac03a5b9aca49e2b63e97f7c0ae0cec    (managing entities and intents)
# client:       e4099166fd7a41218ba851d21e6866f5    (making queries)
# Authorization: Bearer YOUR_ACCESS_TOKEN

def async_read_microphone():
    recognizer_instance = Recognizer()
    recognizer_instance.energy_threshold = SENSITIVITY # TODO: modify sensitivity
    recognizer_instance.phrase_time_limit = 20 # TODO: I don't think this variable is working
                                               #       find out how to change phrase time limit.
                                               #       Do we want this phrase time_limit?
    audio_source = Microphone()
    print("Spawning reader")
    stop_listener_fn = \
        recognizer_instance.listen_in_background( \
            audio_source, asynch_listener_fn)

    print("Leaving read microphone")
    """print("Waiting to read for 10 seconds")
    from time import sleep
    sleep(100)                  # TODO: when do we stop lisening?
    stop_listener_fn()          #       Probably never; Maybe when we
                                #       just quit out of app?
    print("No longer taking audio input")
    
    return
    """


def sync_read_microphone(duration = 5):
    global some_structure, voice_function
    with Microphone() as audio_source:
        recognizer_instance = Recognizer()
        recognizer_instance.energy_threshold = SENSITIVITY

        print("Reading")
        audio_data = \
            recognizer_instance.record( \
                audio_source, duration = duration)

        print("Performing Sphinx Speech to Text")
        try:
            text_from_audio = \
                recognizer_instance.recognize_sphinx( \
                    audio_data, show_all = False)
        except Exception as e:
            print(
                "Exception in recognizer: " + str(e))
            text_from_audio = None

        print(text_from_audio)
        print("Sending HTTP request to API AI")
        # TODO: send this text to Alina's API.AI using a GET request
        some_structure = \
            get('https://api.api.ai/v1/query?v=20150910&query=%s&lang=en&sessionId=1234567890' % text_from_audio,
                headers={
                    'language-tag'  : 'en',
                    'Authorization' : 'Bearer e4099166fd7a41218ba851d21e6866f5',
                    'Content-Type'  : 'application/json; charset=utf-8'
                }
            )
        print("Got structure back:")
        try: prettyprinter.pprint(some_structure.json())
        except: print("Could not print JSON result.")

        try:
            voice_function = eval(some_structure.json()['result']['metadata']['intentName'])
            if not callable(voice_function):
                assert(False)
        except Exception as err:
            print("Not a valid voice function", voice_function)
            print("Exception: {0}".format(err))
            voice_function = None
    return None