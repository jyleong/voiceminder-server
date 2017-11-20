## Socket Instance to hold global dictionary of all in current use sockets,
## should only have aone member variable dictionary of socket instances


class SocketInstances(object):
    __instance = None
    socketStorage = dict()
    namedSocketIDs = dict()
    def __new__(cls):
        if SocketInstances.__instance is None:
            SocketInstances.__instance = object.__new__(cls)

        return SocketInstances.__instance

    @staticmethod
    def getSocketIdByName(name):
      return SocketInstances.namedSocketIDs.get(name, None)

    @staticmethod
    def getSocketInstanceByName(name):
      socketId = SocketInstances.getSocketIdByName(name)
      print(socketId)
      # print(type(SocketInstances.socketStorage))
      print(SocketInstances.socketStorage)
      socket = SocketInstances.socketStorage[socketId]
      print(socket)
      return socket

    @staticmethod
    def setSocketIdByName(socketId, name):
      SocketInstances.namedSocketIDs[name] = socketId
