import speech_recognition
from gtts import gTTS
import os
import queue

import websocket
# from threading import Thread
# import time
# import sys
# import argparse

# USER_NAME = ""
# TEST_MODE = False

speaking = False

from enum import Enum
class ClientState(Enum):
    Deciding = 0
    Speaking = 1
    Listening = 2
    Invalid = 99



def speak(incomingtext):
    speaking = True
    print(incomingtext)
    tts = gTTS(text=incomingtext, lang='en')
    tts.save("incomingtext.mp3")
    os.system("mpg321 incomingtext.mp3")
    speaking = False

recognizer = speech_recognition.Recognizer()
def listen():
    with speech_recognition.Microphone() as source:
        # recognizer.energy_threshold = 150
        # recognizer.adjust_for_ambient_noise(source, duration= 0.5)
        
        recognizer.dynamic_energy_threshold = True

        audio = recognizer.listen(source, timeout=300, phrase_time_limit=1000)

    try:
        # print(recognizer.recognize_sphinx(audio))
        # return recognizer.recognize_sphinx(audio)
        print(recognizer.recognize_google(audio))
        return recognizer.recognize_google(audio)
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
    except speech_recognition.UnknownValueError:
        print("Could not understand audio, trying again")
    except speech_recognition.RequestError as e:
        print("Recog Error; {0}".format(e))

    return ""

def on_error(ws, error):
    print(error)

def on_close(ws):
    speak("closed")
    print("### closed ###")

def on_message(ws, message):
    print('client on_message: enqueuing message')
    globalQueue.put(message)


def on_open(ws):
    print("client is opening")
    # TODO Refactor
    clientState = ClientState.Deciding
    handleDecidingState(ws)

def handleDecidingState(ws):
    if not globalQueue.empty():
        print("handleDecidingState: setting state to speaking")
        # TODO Refactor
        clientState = ClientState.Speaking
        handleSpeakingState()
    else:
        print("handleDecidingState: setting state to Listening")
        # TODO Refactor
        clientState = ClientState.Listening
        handleListeningState(ws)

def handleListeningState(ws):
    print("handleListeningState: setting state to Listening")
    raw = listen()
    if raw:
        ws.send(raw)
        completeListeningState()

def completeListeningState():
    clientState = ClientState.Speaking
    handleSpeakingState()


def handleSpeakingState():
    print("handleSpeakingState: dequeueing messages")
    print(globalQueue.get())
    speak(globalQueue.get())

if __name__ == "__main__":
    global globalQueue 
    globalQueue = queue.Queue()

    host = "ws://voiceminder.localtunnel.me/websocket/"
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
