import uuid
from tornado.websocket import WebSocketHandler
from sockets.socket_instances import SocketInstances
from textProcessing.ProcessText import ProcessingState, ProcessText
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

    def currentUser(self):
        return UserList.userFromSocket(self)

    def on_message(self, str):
        #TODO: get user instance, given socket
        print("on_message: ", str)
        # guard
        user = self.currentUser()
        if user is None:
            self.write_message('Fatal Error, user is None')
            return
        state = user.state
        if state is UserState.Invalid:
            self.write_message('Invalid state, start over')
            return

        if state is UserState.Nameless:
            self.handleNamelessState(user, str)
        elif state is UserState.NameStaging:
            self.handleNameStagingState(user, str)
        elif state is UserState.Ready:
            self.handleReadyState(user, str)
        elif state is UserState.Conversing:
            self.handleConversingState(user, str)
        else:
            self.write_message('Invalid state, start over')
        return

    def on_close(self):
        SocketInstances.socketStorage.pop(self.id, 0)
        print("Socket closed.")

    def handleNamelessState(self, user, str):
        name = ProcessText.getUserName(str)
        if name is not None:
            self.confirmName(name)
            user.state = UserState.NameStaging
        else:
            self.askForName()

    def confirmName(self, name):
        self.write_message(f"Is your name {name}?")
        user = self.currentUser()
        user.name = name
        user.state = UserState.NameStaging
        #TODO: put a timer on user on a thread and callback to check back on user


    def handleNameStagingState(self, user, str):
        if ProcessText.isAffirmative(str):
            user.state = UserState.Ready
            self.write_message(f"Hello {user.name}, now ready to send messages")
        else:
            user.state = UserState.Nameless
            self.askForName()

    def handleReadyState(self, user, str):
        print("handleReadyState")
        pass

    def handleConversingState(self, user, str):
        print("handleConversingState")
        pass

