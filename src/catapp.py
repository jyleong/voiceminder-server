from enum import Enum
import urllib.request
import json

class CatState(Enum):
    Active = 0
    Banned = 1

class CatApp:

    def __init__(self):
        self.userState = CatState.Active
        self.catsdict = None
        self.ctr = 0


    def handle(self, incomingtext):
        if self.userState == CatState.Active:
            someDict = dict()
            lowerText = incomingtext.lower()
            if lowerText == "cat":
                someDict = self.showCat()
            elif lowerText == "dog":
                someDict = self.permaban()
            elif lowerText == "i don't like cats":
                someDict = self.leave()
            else:
                someDict = {"actionType":"nothing"}
            return someDict
        else:
            return {"actionType":"nothing"}

    def getCatPicture(self):
        picUrl = ""

        if self.catsdict is None:
            urllib.request.urlopen("https://www.reddit.com/r/catsstandingup/.json")
            catjson = urllib.request.urlopen("https://www.reddit.com/r/catsstandingup/.json").read()
            self.catsdict = json.loads(catjson)
            print("fetching cats")


        i = self.ctr % len(self.catsdict['data']['children'])
        picUrl = self.catsdict['data']['children'][i]['data']['url']
        self.ctr += 1

        #this is the first cat picture.
        return picUrl
        #return catdict['data']['children'][0]['data']['url']

    #all three of these should return JSON themselves.
    def showCat(self):
        catDict = dict()
        catDict["actionType"] = "show_image"
        actionDetail = dict()
        actionDetail["url"] = self.getCatPicture()
        #make a json call for a cat image.
        catDict["actionDetail"] = actionDetail
        #display a cat picture
        return catDict

    def permaban(self):
        #display a 'you are banned' sad cat picture
        #it is up the user to say 'take me home' to exit.banDict = dict()
        banDict = dict()
        banDict["actionType"] = "show_image"
        actionDetail = dict()
        actionDetail["url"] = "www.catbanpicture.com"
        banDict["actionDetail"] = actionDetail
        self.userState = CatState.Banned
        return banDict

    def leave(self):
        leaveDict = dict()
        leaveDict["actionType"] = "leave"
        actionDetail = dict()
        actionDetail["actionDetail"] = actionDetail
        return leaveDict
        #go up one level, not home.
