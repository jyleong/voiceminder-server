import uuid
from tornado.websocket import WebSocketHandler
from sockets.socket_instances import SocketInstances

class WebSocket(WebSocketHandler):
    def open(self):
        self.id = str(uuid.uuid4())
        SocketInstances.socketStorage[self.id] = self

    def on_message(self, str):
        # TODO check str enum type, 
        # if type is recognition, set socket.
        # if type is send message, get socket 

        print("message: ", str)
        # name = getUserName(message)
        # usermessage = getUsermessage(message)

        # echo message to everyone except self
        for k, v in SocketInstances.socketStorage.items():
            print("id: {}, socket instance: {}".format(k,v))
            if k != self.id:
                print("writing message")
                #TODO refactor into usermessage
                v.write_message(str)
        
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
