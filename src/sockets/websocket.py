import uuid

from tornado.websocket import WebSocketHandler

from sockets.socket_instances import SocketInstances


class WebSocket(WebSocketHandler):
    def open(self):
        self.id = uuid.uuid4()
        SocketInstances.socket_storage[self.id] = {'socketInstance': self}
        print("New connection. Socket opened. Assigned socket id: {}".format(SocketInstances.socket_storage[self.id]['id']))

    def on_message(self, message):
        # Some message parsing here

        # search message for persons name/ or id to know who to send to
        self.write_message("Received: " + message)
        for k, v in SocketInstances.socket_storage.items():
            print("id: {}, socket instance: {}".format(k,v))
            # if (k == idToWrite):
            #     v['socketInstance'].write_message(message)
            # get the person/id you want to send message to
            # if the key (id) == person's id send message to them
        print("Received message: " + message)

    def on_close(self):
        SocketInstances.socket_storage.remove(self.id)
        print("Socket closed.")
