class CatApp:
    #when we say cat, gives us a cat picture.
        #dog, exits the app / bans the user.
        #else, tells the user to say cat.

    #Out: some action - if cat, json pointing to an image of a cat, if dog, pointing to some 'banned' dog picture.


    #in terms of json, can just grab from /r/subreddit.json
        #need the ability to parse json, this should be generic.
    def handle(incomingtext):
        someDict = dict()
        lowerText = incomingtext.lower()
        if lowerText == "cat":
            showCat()
        elif lowerText == "dog":
            permaban()
        elif lowerText == "i don't like cats":
            leave()
        else:
            #ask for clarification of some sort.  "say cat or dog."
        #in: A string with what the user has said.
        #did it say cat? dog? else?
        #somedict key: the action type
        #       value: diplay image OR ban user OR quit ("I dont like cats anymore", not "take me home")

        {
        actionType: "speak"
        actionDetail: {
        phrase: "say cat or dog"
            }
        }

        {
        actionType: "show_image"
        actionDetail: {
        url: "www.imgur.com/fjifaewjioaewjifajifeawji"
            }
        }

        return someDict

    def getCatPicture():
        #json call
        #pick a random picture
        picUrl = ""
        return picUrl

    #all three of these should return JSON themselves.
    def showCat():
        catDict = dict()
        catDict["actionType"] = "show_image"
        actionDetail = dict()
        actionDetail["url"] = "www.somecatpicture.com"
        #make a json call for a cat image.
        catDict["actionDetail"] = actionDetail
        #display a cat picture
        getCatPicture()
        #prepare for displaying more pictures

        return someDict

    def permaban():
        #display a 'you are banned' sad cat picture
        #it is up the user to say 'take me home' to exit.

    def leave():
        #go up one level, not home.
