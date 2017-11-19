import json

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
    def getUserName(self, userInput):
        inputlist = userInput.split()

        recipientName = inputlist[3]

        return "Hello {}".format(recipientName)


    """
        take in a string: "hi june can you pick up some cheese"
        Understand the hello and name, extract name and message
        will need NLP properly here
    """
    def getNameandMessage(self, userInput):
        inputlist = userInput.split()

        recipientName = inputlist[1]
        message = ' '.join(inputlist[2:])

        print('recipientName:', recipientName)
        print('message:', message)

        return json.dumps({'recipient_Name': recipientName, 'message': message})