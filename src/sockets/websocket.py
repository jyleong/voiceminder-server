import uuid

from tornado.websocket import WebSocketHandler

from sockets.socket_instances import SocketInstances


class WebSocket(WebSocketHandler):
    def open(self):
        self.id = uuid.uuid4()
        SocketInstances.socket_storage[self.id] = self
        print("open self.id: {}".format(self.id))

    def on_message(self, message):
        print("on_message self.id: {}".format(self.id))

        # Some message parsing here 
        # if message.type == 'set_group':
        #     SocketInstances.socket_storage[self.id]['group'] = message.group
        self.write_message("Received: " + message)
        print("Received message: " + message)
        print("number of sockets in SocketInstances: ", len(SocketInstances.socket_storage))

    def on_close(self):
        SocketInstances.socket_storage.pop(self.id, 0)
        print("Socket closed.")
