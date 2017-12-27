import speech_recognition
from gtts import gTTS
import os

import websocket
# from threading import Thread
# import time
# import sys
# import argparse

# USER_NAME = ""
# TEST_MODE = False

speaking = False

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
    queue = []
    if speaking:
        speak(message)
    else:
        queue.enque(message)
        # when speaking set back to true, deque and speak the message
        # when message is done speaking, set speaking back to false

def on_open(ws):
    while True:
        if not speaking:
            raw = listen()
            # when listen is complete, set speaking back to true
            if raw:
                ws.send(raw)
    #handle ping later 

if __name__ == "__main__":
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
