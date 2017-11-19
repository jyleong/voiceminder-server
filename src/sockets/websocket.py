import uuid

from tornado.websocket import WebSocketHandler

from sockets.socket_instances import SocketInstances


class WebSocket(WebSocketHandler):
    def open(self):
        self.id = uuid.uuid4()
        SocketInstances.socket_storage[self.id] = {'id': self.id}
        print("New connection. Socket opened. Assigned socket id: {}".format(SocketInstances.socket_storage[self.id]['id']))

    def on_message(self, message):
        # Some message parsing here
        if message.type == 'set_group':
            SocketInstances.socket_storage[self.id]['group'] = message.group
        self.write_message("Received: " + message)
        print("Received message: " + message)

    def on_close(self):
        SocketInstances.socket_storage[self.id].remove(self.id)
        print("Socket closed.")
