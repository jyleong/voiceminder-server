import speech_recognition
from gtts import gTTS
import os
def speak(incomingtext):
	print(incomingtext)
	tts = gTTS(text=incomingtext, lang='en')
	tts.save("incomingtext.mp3")
	os.system("mpg321 incomingtext.mp3")

import websocket
from threading import Thread
import time
import sys


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        while True:
            raw = input()
            ws.send(raw)
    runThread = Thread(target=run)
    runThread.daemon = False
    runThread.start()

    def ping(*args):
        while True:
            time.sleep(1)
            ws.send("ping")

    Thread(target=ping).start()


if __name__ == "__main__":
    # websocket.enableTrace(True)
    if len(sys.argv) < 2:
        host = "ws://voiceminder.localtunnel.me/websocket/"
    else:
        host = sys.argv[1]
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
