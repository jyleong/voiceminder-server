import uuid
from tornado.websocket import WebSocketHandler
from sockets.socket_instances import SocketInstances

class WebSocket(WebSocketHandler):
    def open(self):
        self.id = str(uuid.uuid4())
        SocketInstances.socketStorage[self.id] = self

    def on_message(self, message):
        print("message: ", message)
        # name = getUserName(message)
        # usermessage = getUsermessage(message)

        # search message for persons name/ or id to know who to send to
        for k, v in SocketInstances.socketStorage.items():
            print("id: {}, socket instance: {}".format(k,v))
            if k != self.id:
                print("writing message")
                #TODO refactor into usermessage
                v.write_message(message)
        
        SocketInstances.setSocketIdByName(self.id, "june")

        #TODO refactor into name
        destination = SocketInstances.getSocketInstanceByName("june")
        print("destination: ", destination)

        #TODO refactor into usermessage
        destination.write_message("june said hey kevin")
        print("number of sockets in SocketInstances: ", len(SocketInstances.socketStorage))

    def on_close(self):
        SocketInstances.socketStorage.pop(self.id, 0)
        print("Socket closed.")
