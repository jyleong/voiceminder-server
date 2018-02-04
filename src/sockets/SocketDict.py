class SocketDict(object):
    __instance = None
    socketsDict = dict()

    def __new__(cls):
        if SocketDict.__instance is None:
            SocketDict.__instance = object.__new__(cls)
        return SocketDict.__instance

    def addSocket(cls, userId, socketInstance):
        cls.socketsDict[userId] = socketInstance

    def findSocketByUserId(cls, userId):
        return cls.socketsDict[userId]

    def deletesocketByUserId(cls, userId):
        cls.socketsDict.pop(userId, None)
        print("Deleted socket by userId " + userId)
        return
