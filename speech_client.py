import speech_recognition
from gtts import gTTS
import os

import websocket
from threading import Thread, Lock
import time
import argparse

SPEAKING = False

THREADLOCK = Lock()

def speak(incomingtext):
    global SPEAKING
    THREADLOCK.acquire() # begin critical section
    SPEAKING = True
    print(incomingtext)
    tts = gTTS(text=incomingtext, lang='en')
    tts.save("incomingtext.mp3")
    os.system("mpg321 incomingtext.mp3")
    SPEAKING = False
    THREADLOCK.release() # end critical section

recognizer = speech_recognition.Recognizer()
def listen():
    with speech_recognition.Microphone() as source:
        # recognizer.energy_threshold = 150
        # recognizer.adjust_for_ambient_noise(source, duration= 0.5)
        
        recognizer.dynamic_energy_threshold = True

        audio = recognizer.listen(source, timeout=300, phrase_time_limit=1000)

    try:
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
    speak(message)

def on_open(ws):
    def deliver(*args):
        global SPEAKING
        while True:
            if not SPEAKING:
                raw = listen()
                print("listen(): " + raw)
                if raw:
                    ws.send(raw)
    runThread = Thread(target=deliver)
    runThread.daemon = False
    runThread.start()

    def ping(*args):
        while True:
            time.sleep(1)
            ws.send("ping")

    Thread(target=ping).start()


if __name__ == "__main__":
    # websocket.enableTrace(True)
    parser = argparse.ArgumentParser(description='Arguments to start speech client')
    parser.add_argument('--host', type=str, default="ws://localhost:5000/websocket/",
                    help='an integer for the accumulator')
    args = parser.parse_args()
    host = args.host
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
