## Socket Instance to hold global dictionary of all in current use sockets,
## should only have one member variable dictionary of socket instances

class SocketInstances(object):
    __instance = None
    socketStorage = dict()
    namedSocketIDs = dict()
    def __new__(cls):
        if SocketInstances.__instance is None:
            SocketInstances.__instance = object.__new__(cls)

        return SocketInstances.__instance

    @staticmethod
    def getSocketIdByName(cls, name):
      socketId = SocketInstances.namedSocketIDs.get(name, None)
      return socketId

    @staticmethod
    def getSocketInstanceByName(cls, name):
      socketId = SocketInstances.getSocketIdByName(name)
      socket = SocketInstances.socketStorage.get(socketId, None)
      return socket

    @classmethod
    def setSocketIdByName(cls, socketId, name):
        SocketInstances.namedSocketIDs[name] = socketId
