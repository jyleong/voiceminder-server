import json
from enum import Enum, auto

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

    Recognition = auto()
    Communication = auto()

    def getEnum(self, userInput):
        inputlist = userInput.split()
        if inputlist[0] == 'hello':
            enum = Recognition
        elif inputlist[0] == 'yo' || inputlist[0] == 'hey'
            enum = Communication
        return enum

    def getUserName(self, userInput):
        inputlist = userInput.split()
        recipientName = inputlist[3]
        return recipientName
        # return "Hello {}".format(recipientName)


    """
        take in a string: "hey june can you pick up some cheese"
        Understand the hey and name, extract name and message
        will need NLP properly here
    """
    def getNameandMessage(self, userInput):
        inputlist = userInput.split()
        recipientName = inputlist[1]
        message = ' '.join(inputlist[2:])
        return recipientName , message

        # return json.dumps({'recipient_Name': recipientName, 'message': message})
