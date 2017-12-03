import uuid
from tornado.websocket import WebSocketHandler
from sockets.socket_instances import SocketInstances
from textProcessing.processing import ProcessingState, ProcessText
from enum import Enum
from user.User import User
from user.User import UserState
from user.user_list import UserList


class WebSocket(WebSocketHandler):

    def askForName(self):
        self.write_message("State your name")

            
    def open(self):
        self.id = str(uuid.uuid4())
        newUser = User()
        newUser.socket = self
        UserList.append(newUser)

        print("UserList.containsUser(newUser): ", UserList.containsUser(newUser))
        # SocketInstances.socketStorage[self.id] = self
        self.askForName()

    def on_message(self, str):
        #TODO: get user instance, given socket
        print("on_message: ", str)
        # guard
        currentUser = UserList.userFromSocket(self)
        if currentUser is None:
            self.write_message('Fatal Error, currentUser is None')
            return
        state = currentUser.state
        if state is UserState.Invalid:
            self.write_message('Invalid state, start over')
            return

        if state is UserState.Nameless:
            self.handleNamelessState(currentUser, str)
        elif state is UserState.NameStaging:
            self.handleNameStagingState(currentUser, str)
        elif state is UserState.Ready:
            self.handleReadyState(currentUser, str)
        elif state is UserState.Conversing:
            self.handleConversingState(currentUser, str)
        else:
            self.write_message('Invalid state, start over')
        return


        # Current user from self/socket
        if UserList.userFromSocket(self) is None:
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
        
        # destination = SocketInstances.getSocketInstanceByName("june")
        # print("destination: ", destination)
        # destination.write_message("june said hey kevin")
        # print("number of sockets in SocketInstances: ", len(SocketInstances.socketStorage))


    def on_close(self):
        SocketInstances.socketStorage.pop(self.id, 0)
        print("Socket closed.")

    def handleNamelessState(self, currentUser, str):
        name = ProcessText.getUserName(str)
        if name is not None:
            self.confirmName(name)
            currentUser.state = UserState.NameStaging
        else:
            self.askForName()
            '''
            self.handleReadyState(currentUser, str)
        elif state is UserState.Conversing:
            self.handleConversingState(currentUser, str)

            '''
    def handleNameStagingState(self, currentUser, str):
        print("handleNameStagingState")
        pass

    def handleReadyState(self, currentUser, str):
        print("handleReadyState")
        pass

    def handleConversingState(self, currentUser, str):
        print("handleConversingState")
        pass

    def confirmName(self, name):
        self.write_message(f"Is your name {name}?")

 