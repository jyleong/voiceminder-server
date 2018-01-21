from enum import Enum
import uuid

class UserState(Enum):
    Nameless = 0
    NameStaging = 1
    Ready = 2
    Conversing = 3
    Invalid = 99

class User(object):

    socket = None
    name = None
    uuid = None
    state = UserState.Nameless
    conversant = None

    """docstring for User"""
    def __init__(self):
        super(User, self).__init__()

    def setState(self, newState):
        self.state = newState
        print("User {} is now in state {}".format(self.name, self.state))

    def setUUID(self, uuid):
        self.uuid = uuid
        print("User's uuid is set!")
    

