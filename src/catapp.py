from enum import Enum
import urllib.request
import json
import requests

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
            if lowerText == "cat" or lowerText == "cats" or lowerText == "got" or lowerText == "chat":
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
            try:
                url = "https://www.reddit.com/r/catsstandingup/.json"
                headers = {'user-agent': 'ChromeCats'}
                r = requests.get(url, headers=headers)
                self.catsdict = r.json()
                print("fetching cats")
            except Exception as e:
                print("Error fetching json: ", e)
                return "https://http.cat/429.jpg"

        i = self.ctr % len(self.catsdict['data']['children'])
        picUrl = self.catsdict['data']['children'][i]['data']['url']
        if picUrl[-1] == "v":
            picUrl = picUrl[:len(picUrl) - 1]
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
        actionDetail["url"] = "https://i.imgflip.com/24rtuf.jpg"
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
