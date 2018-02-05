class Conversation(object):
    ## first will be the one that initiates the conversation
    userFirst = None
    userSecond = None

    def __init__(self, userFirst, userSecond):
        self.userFirst = userFirst
        self.userSecond = userSecond