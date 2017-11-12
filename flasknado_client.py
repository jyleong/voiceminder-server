#!/usr/bin/python

from websocket import create_connection
ws = create_connection("ws://localhost:5000/websocket/")
print("Sending 'Hello, World'...")
ws.send("Hello, World")
print("Sent")
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)
ws.close()