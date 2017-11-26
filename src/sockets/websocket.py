import uuid
from tornado.websocket import WebSocketHandler
from sockets.socket_instances import SocketInstances
from textProcessing.processing import ProcessingState, ProcessText
from enum import Enum
from user.User import User
from user.user_list import UserList

class SocketState(Enum):
    Nameless = 1
    NameStaging = 2
    Ready = 3

class WebSocket(WebSocketHandler):
    def getSocketState(self):
        pass
            

    def open(self):
        self.id = str(uuid.uuid4())
        newUser = User()
        newUser.socket = self
        UserList.append(newUser)

        print("UserList.containsUser(newUser): ", UserList.containsUser(newUser))
        # SocketInstances.socketStorage[self.id] = self
        self.write_message("State your name")

    def on_message(self, str):
        #TODO: get user instance, given socket
        print("on_message: ", str)
        # Current user from self/socket
        if SocketInstances.getNameFromSocket(self) is None:
            userName = ProcessText.getUserName(str)
            SocketInstances.setSocketIdByName(self.id, userName)
            self.write_message("Is your name " + userName)
            return
        enum = ProcessText.getEnum(str)
        if enum == ProcessingState.Recognition:
            username = ProcessText.getUserName(str)
            SocketInstances.setSocketIdByName(self.id, username)
        elif enum == ProcessingState.Communication:
            recipientName , message = ProcessText.getNameandMessage(str)
            destination = SocketInstances.getSocketInstanceByName(recipientName)
            destination.write_message(message)
        else:
            print("doing nothing in the else case")
        
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
