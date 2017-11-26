
from enum import Enum

class ProcessingState(Enum):
    Recognition = 1
    Communication = 2

class ProcessText(object):
    """
    Class of text processing methods in python
    """

    """
        take in a string like "Hi I'm June"
        or "my name is June" <
        and extract the name
        will need NLP properly here
    """
    @staticmethod
    def getEnum(userInput):
        inputlist = userInput.split()
        greeting = inputlist[0].lower()
        enum = 0
        if greeting == 'hello':
            enum = ProcessingState.Recognition
        elif greeting == 'yo' or greeting == 'hey':
            enum = ProcessingState.Communication
        return enum

    @staticmethod
    def getUserName(userInput):
        inputlist = userInput.split()
        recipientName = inputlist[3].lower()
        return recipientName
        # return "Hello {}".format(recipientName)


    """
        take in a string: "hey june can you pick up some cheese"
        Understand the hey and name, extract name and message
        will need NLP properly here
    """
    @staticmethod
    def getNameandMessage(userInput):
        inputlist = userInput.split()
        recipientName = inputlist[1]
        message = ' '.join(inputlist[2:])
        return recipientName , message

