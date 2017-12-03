
from enum import Enum

class ProcessingState(Enum):
    Recognition = 1
    Communication = 2

class ProcessText(object):
    """
    Class of text processing methods in python
    """
    @staticmethod
    def isSelfIdentification(userInput):
        
        return True

    @staticmethod
    def isUserMessaging(userInput):
        return True

    """
        take in a string like "Hi I'm June"
        or "my name is June" <
        and extract the name
        will need NLP properly here
    """
    @staticmethod
    def getEnum(userInput):
        print("getEnum: ", userInput)
        if ProcessText.isSelfIdentification(userInput):
            print("isSelfIdentification")
            enum = ProcessingState.Recognition
        elif ProcessText.isUserMessaging(userInput):
            print("isUserMessaging")
            enum = ProcessingState.Communication
        return enum

    @staticmethod
    def getUserName(userInput):
        if userInput is None or "": return None
        print("getUserName: ", userInput)
        # assume that the last word of userInput 
        inputlist = userInput.split()
        recipientName = inputlist[-1].lower()
        return recipientName

    @staticmethod
    def isAffirmative(userInput):
        inputList = userInput.split()
        affirmativeList = ['yes', 'yep', 'ya', 'correct', 'right']
        for word in inputList:
            if word in affirmativeList:
                return True
        return False
            
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

