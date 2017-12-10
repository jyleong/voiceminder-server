import uuid
from tornado.websocket import WebSocketHandler
from textProcessing.ProcessText import ProcessingState, ProcessText
from enum import Enum
from user.User import User
from user.User import UserState
from user.user_list import UserList
import threading

class WebSocket(WebSocketHandler):

    def askForName(self):
        self.write_message("State your name")

    def open(self):
        self.id = str(uuid.uuid4())
        newUser = User()
        newUser.socket = self
        UserList.append(newUser)

        self.askForName()

    def currentUser(self):
        return UserList.userFromSocket(self)

    def on_message(self, str):
        if str == "ping": return
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
        # find user by socket
        user = self.currentUser()
        UserList.deleteUserBySocket(user.socket)

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
        self.beginCountdown(name)

    def beginCountdown(self, name):
        countdownTimer = threading.Timer(4, function=self.confirmName, args=(name,))
        countdownTimer.start()
      
    def stopCountdown(self):
        allThreads = threading.enumerate()
        main = threading.main_thread()
        for t in allThreads:
            if t is not main:
                t.cancel()

    def handleNameStagingState(self, user, str):
        if (not str):
            self.confirmName(user.name)
            return

        if ProcessText.isAffirmative(str):
            self.stopCountdown()
            user.state = UserState.Ready
            self.write_message(f"Hello {user.name}, now ready to send messages")
        else:
            self.stopCountdown()
            user.state = UserState.Nameless
            self.askForName()

    def handleReadyState(self, user, str):
        print("handleReadyState")
        # process str, cases: outgoing, i dont understand
        recipientName, message = ProcessText.getNameandMessage(str)
        if not message:
            message = str
        messageSuccess = self.messageNamedUser(user, recipientName, message)        
        if messageSuccess:
            user.state = UserState.Conversing
            # pseudocode alert!
            user.conversant = UserList.userFromName(recipientName)
            user.conversant.conversant = user
            user.conversant.state = UserState.Conversing
            # TODO: user needs to remember currentRecipient  
            # TODO: set timer on UserState, if no message for 30 seconds, then back to ready

    def messageNamedUser(self, user, recipientName, message):
        if not recipientName:
            self.write_message("could not recognize the recipient in your message")
            return False
        recipient = UserList.userFromName(recipientName)
        if not recipient:
            self.write_message("could not find the recipient from your message")
            return False

        print("user.name:", user.name)
        print("message:", message)

        recipient.socket.write_message(f"{user.name} says, {message}")
        
        return True

    def handleConversingState(self, user, str):
        print("handleConversingState")
        # if different from the one conversing with now, then switch.
        if ProcessText.hasRecipientName(str):
            recipientName, message = ProcessText.getNameandMessage(str)
            messageNamedUser(recipientName, message)        
        else:
            user.conversant.socket.write_message(str)

