import uuid
from tornado.websocket import WebSocketHandler
from sockets.socket_instances import SocketInstances
from textProcessing.processing import ProcessingState, ProcessText

class WebSocket(WebSocketHandler):
    def open(self):
        self.id = str(uuid.uuid4())
        SocketInstances.socketStorage[self.id] = self

    def on_message(self, str):
        enum = ProcessText.getEnum(str)
        if enum == ProcessingState.Recognition:
            username = ProcessText.getUserName(str)
            SocketInstances.setSocketIdByName(self.id, username)
        elif enum == ProcessingState.Communication:
            recipientName , message = ProcessText.getNameandMessage(str)
            destination = SocketInstances.getSocketInstanceByName(recipientName)
            destination.write_message(message)
        print("message: ", str)
        
        # # echo message to everyone except self
        # for k, v in SocketInstances.socketStorage.items():
        #     print("id: {}, socket instance: {}".format(k,v))
        #     if k != self.id:
        #         print("writing message")
        #         #TODO refactor into usermessage
        #         v.write_message(str)
        
        # SocketInstances.setSocketIdByName(self.id, "june")

        # destination = SocketInstances.getSocketInstanceByName("june")
        # print("destination: ", destination)
        # destination.write_message("june said hey kevin")
        # print("number of sockets in SocketInstances: ", len(SocketInstances.socketStorage))

    def on_close(self):
        SocketInstances.socketStorage.pop(self.id, 0)
        print("Socket closed.")
