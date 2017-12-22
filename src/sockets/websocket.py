from tornado.websocket import WebSocketHandler
from textProcessing.ProcessText import ProcessText
from asynchronous.countdown import EventLoop, Countdown
from user.User import User, UserState
from user.user_list import UseFzrList

class WebSocket(WebSocketHandler):

    def askForName(self):
        self.write_message("Please state your name:")

    def open(self):
        print("SERVER: On new connection!")
        self.eventLoop = None
        self.countDown = None
        UserList.append(User(self))
        self.askForName()

    def currentUser(self):
        return UserList.userFromSocket(self)

    def on_message(self, str):
        if str == "ping": return
        #TODO: get user instance, given socket
        print("on_message: ", str)
        # guard
        testing = ProcessText.checkTestingMode(str)

        user = self.currentUser()
        if testing:
            print("SERVER: In testing mode")
            name = ProcessText.getUserName(str)
            user.name = name
            user.state = UserState.Ready

        if user is None:
            self.write_message('Fatal Error! User is None.')
        if user.state is UserState.Invalid:
            self.write_message('Invalid state! Start over.')
        elif user.state is UserState.Nameless:
            self.handleNamelessState(user, str)
        elif user.state is UserState.NameStaging:
            self.handleNameStagingState(user, str)
        elif user.state is UserState.Ready:
            self.handleReadyState(user, str)
        elif user.state is UserState.Conversing:
            self.handleConversingState(user, str)
        else:
            self.write_message('Invalid state, start over')
        return

    def on_close(self):
        user = self.currentUser()
        UserList.deleteUserBySocket(user.socket)
        print("Socket closed.")

    def handleNamelessState(self, user, str):
        name = ProcessText.getUserName(str)
        if name is not None:
            self.eventLoop = EventLoop(lambda: self.confirmName(name))
            self.eventLoop.start()
            user.state = UserState.NameStaging
        else:
            self.askForName()

    def confirmName(self, name):
        self.write_message(f"Is your name {name}?")
        user = self.currentUser()
        user.name = name
        user.state = UserState.NameStaging

    def handleNameStagingState(self, user, str):
        # empty string case also handled by client
        if (not str):
            self.eventLoop = EventLoop(lambda: self.confirmName(user.name))
            self.eventLoop.start()
            return
        
        self.eventLoop.stop()
        self.eventLoop = None
        
        if ProcessText.isAffirmative(str):
            user.state = UserState.Ready
            self.write_message(f"Hello {user.name}, now ready to send messages")
        else:
            user.state = UserState.Nameless
            self.askForName()

    def handleReadyState(self, user, str):
        #check existence of name and message
        if not ProcessText.hasNameandMessage(str):
            self.write_message("Who is the recipient, and what is your message?")
            return

        recipientName, message = ProcessText.getNameandMessage(str)
        if not message:
            # message body is empty, just copy whole input to message
            message = str

        messageSuccess = self.messageNamedUser(user, recipientName, message)        
        if messageSuccess:
            user.state = UserState.Conversing
            # when timer runs out, setState to UserState.Ready
            print('messageSuccess, begin Conversing countDown')
            self.countDown = Countdown(lambda: user.setState(UserState.Ready), duration=10)
            self.countDown.start()
        
    def messageNamedUser(self, user, recipientName, message):
        if not recipientName:
            self.write_message("could not recognize the recipient in your message")
            return False
        
        recipient = UserList.userFromName(recipientName)
        
        if not recipient:
            self.write_message("could not find the recipient from your message")
            return False

        # terminate conversation on other end if switching to new recipient
        if user.conversant is not None and user.conversant != recipient:
            user.conversant.conversant = None
            user.conversant.state = UserState.Ready

        # handle multi way conversation between users
        user.conversant = recipient
        user.conversant.conversant = user
        user.conversant.state = UserState.Conversing
        
        recipient.socket.write_message(f"{user.name} says, {message}") 
        return True

    def handleConversingState(self, user, str):
        print("handleConversingState user: {}".format(user.name))
        self.restartCountDown(user)
        if ProcessText.hasRecipientName(str):
            recipientName, message = ProcessText.getNameandMessage(str)
            if not message:
                message = str
            self.messageNamedUser(user, recipientName, message)
        else:
            user.conversant.socket.write_message(str)

    def restartCountDown(self, user):
        # cancels the previous countDown,
        print("COUNTDOWN: Stopping previous thread")
        if self.countDown:
            self.countDown.stop()
            self.countDown = None

        # restart countDown
        print("restartCountDown: making new instance")
        self.countDown = Countdown(lambda: user.setState(UserState.Ready), duration=10)
        self.countDown.start()
